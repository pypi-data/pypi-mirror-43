import json
import os
import sys
import time
import requests

from gql import gql
import six

import wandb
from wandb import util
from wandb import data_types
from wandb.meta import Meta
from wandb.apis.internal import Api

DEEP_SUMMARY_FNAME = 'wandb.h5'
RUNSTATE_FNAME = 'wandb-run.json'
SUMMARY_FNAME = 'wandb-summary.json'
H5_TYPES = ("numpy.ndarray", "tensorflow.Tensor", "pytorch.Tensor")

h5py = util.get_module("h5py")
np = util.get_module("numpy")


class Summary(object):
    """Used to store summary metrics during and after a run."""

    def __init__(self, run, summary=None):
        self._run = run
        self._summary = summary or {}
        self._h5_path = os.path.join(self._run.dir, DEEP_SUMMARY_FNAME)
        # Lazy load the h5 file
        self._h5 = None
        self._locked_keys = set()
        self._run_state = None

    def _write(self, commit=False):
        raise NotImplementedError

    def _transform(self, k, v=None, write=True):
        """Transforms keys json into rich objects for the data api"""
        if not write and isinstance(v, dict):
            if v.get("_type") in H5_TYPES:
                return self.read_h5(k, v)
            elif v.get("_type") == 'parquet':
                print(
                    'This dataframe was saved via the wandb data API. Contact support@wandb.com for help.')
                return None
            # TODO: transform wandb objects and plots
            else:
                return {key: self._transform(k + "." + key, value, write=False) for (key, value) in v.items()}

        return v

    def __getitem__(self, k):
        return self._transform(k, self._summary[k], write=False)

    def __setitem__(self, k, v):
        key = k.strip()
        self._summary[key] = self._transform(key, v)
        self._locked_keys.add(key)
        self._write()

    def __setattr__(self, k, v):
        if k.startswith("_"):
            super(Summary, self).__setattr__(k, v)
        else:
            key = k.strip()
            self._summary[key] = self._transform(key, v)
            self._locked_keys.add(key)
            self._write()

    def __getattr__(self, k):
        if k.startswith("_"):
            return super(Summary, self).__getattr__(k)
        else:
            return self._transform(k.strip(), self._summary[k.strip()], write=False)

    def __delitem__(self, k):
        val = self._summary[k.strip()]
        if isinstance(val, dict) and val.get("_type") in H5_TYPES:
            if not self._h5:
                wandb.termerror("Deleting tensors in summary requires h5py")
            else:
                del self._h5["summary/" + k.strip()]
                self._h5.flush()
        del self._summary[k.strip()]
        self._write()

    def __repr__(self):
        return str(self._summary)

    def keys(self):
        return self._summary.keys()

    def get(self, k, default=None):
        return self._summary.get(k.strip(), default)

    def write_h5(self, key, val):
        # ensure the file is open
        self.open_h5()

        if not self._h5:
            wandb.termerror("Storing tensors in summary requires h5py")
        else:
            try:
                del self._h5["summary/" + key]
            except KeyError:
                pass
            self._h5["summary/" + key] = val
            self._h5.flush()

    def read_h5(self, key, val=None):
        # ensure the file is open
        self.open_h5()

        if not self._h5:
            wandb.termerror("Reading tensors from summary requires h5py")
        else:
            return self._h5.get("summary/" + key, val)

    def open_h5(self):
        if not self._h5 and h5py:
            self._h5 = h5py.File(self._h5_path, 'a', libver='latest')

    @property
    def _run_state_path(self):
        return os.path.join(self._run.dir, RUNSTATE_FNAME)

    def _get_run_state(self):
        if self._run_state is None:
            try:
                self._run_state = json.loads(open(self._run_state_path).read())
            except IOError:
                return None
        return self._run_state

    def _set_run_state(self, run_state_id, summary_dict):
        if self._get_run_state():
            return  # TODO(adrian): we only allow one run state for now

        self._run_state = {
            'wandb_run_id': self._run.name,
            'wandb_run_state_id': run_state_id,
            'summary': summary_dict,
            'config': {k: v['value'] for k, v in self._run.config.as_dict().items()}
        }

        with open(self._run_state_path, 'w') as of:
            json.dump(self._run_state, of)

    def convert_json(self, obj=None, root_path=[]):
        """Convert obj to json, summarizing larger arrays in JSON and storing them in h5."""
        res = {}
        obj = obj or self._summary

        saved_bq_data = False
        run_state = self._get_run_state() or {}
        run_state_id = run_state.get(
            'wandb_run_state_id') or util.generate_id()

        for key, value in six.iteritems(obj):
            path = ".".join(root_path + [key])
            if isinstance(value, dict):
                res[key], converted = util.json_friendly(
                    self.convert_json(value, root_path + [key]))
            elif util.can_write_dataframe_as_parquet() and util.is_pandas_dataframe(value):
                path = util.write_dataframe(
                    value,
                    self._run.name,
                    run_state_id,
                    self._run.dir,
                    key)

                res[key] = {
                    "_type": "parquet",
                    'run_state_id': run_state_id,
                    'current_project_name': self._run.project,  # we don't have the project ID here
                    'path': path,
                }

                saved_bq_data = True
            else:
                tmp_obj, converted = util.json_friendly(
                    data_types.val_to_json(key, value))
                res[key], compressed = util.maybe_compress_summary(
                    tmp_obj, util.get_h5_typename(value))
                if compressed:
                    self.write_h5(path, tmp_obj)

        if saved_bq_data:
            self._set_run_state(run_state_id, res)

        self._summary = res
        return res

    def update(self, key_vals=None, overwrite=True):
        # Passing overwrite=True locks any keys that are passed in
        # Locked keys can only be overwritten by passing overwrite=True
        summary = {}
        if key_vals:
            for k, v in six.iteritems(key_vals):
                key = k.strip()
                if overwrite or key not in self._summary or key not in self._locked_keys:
                    summary[key] = self._transform(k.strip(), v)
                if overwrite:
                    self._locked_keys.add(key)
        self._summary.update(summary)
        self._write(commit=True)


def download_h5(run, entity=None, project=None, out_dir=None):
    api = Api()
    meta = api.download_url(project or api.settings(
        "project"), DEEP_SUMMARY_FNAME, entity=entity or api.settings("entity"), run=run)
    if meta and 'md5' in meta and meta['md5'] is not None:
        # TODO: make this non-blocking
        wandb.termlog("Downloading summary data...")
        path, res = api.download_write_file(meta, out_dir=out_dir)
        return path


def upload_h5(file, run, entity=None, project=None):
    api = Api()
    wandb.termlog("Uploading summary data...")
    api.push({os.path.basename(file): open(file, 'rb')}, run=run, project=project,
             entity=entity)


class FileSummary(Summary):
    def __init__(self, run):
        super(FileSummary, self).__init__(run)
        self._fname = os.path.join(run.dir, SUMMARY_FNAME)
        self.load()

    def load(self):
        try:
            self._summary = json.load(open(self._fname))
        except (IOError, ValueError):
            self._summary = {}

    def _write(self, commit=False):
        # TODO: we just ignore commit to ensure backward capability
        with open(self._fname, 'w') as f:
            s = util.json_dumps_safer(self.convert_json(), indent=4)
            f.write(s)
            f.write('\n')
        if self._h5:
            self._h5.close()
            self._h5 = None


class HTTPSummary(Summary):
    def __init__(self, run, client, summary=None):
        super(HTTPSummary, self).__init__(run, summary=summary)
        self._run = run
        self._client = client
        self._started = time.time()

    def _write(self, commit=False):
        mutation = gql('''
        mutation UpsertBucket( $id: String, $summaryMetrics: JSONString) {
            upsertBucket(input: { id: $id, summaryMetrics: $summaryMetrics}) {
                bucket { id }
            }
        }
        ''')
        if commit:
            if self._h5:
                self._h5.close()
                self._h5 = None
            res = self._client.execute(mutation, variable_values={
                'id': self._run.storage_id, 'summaryMetrics': util.json_dumps_safer(self.convert_json())})
            assert res['upsertBucket']['bucket']['id']
            entity, project, run = self._run.path
            if os.path.exists(self._h5_path) and os.path.getmtime(self._h5_path) >= self._started:
                upload_h5(self._h5_path, run, entity=entity, project=project)
        else:
            return False
