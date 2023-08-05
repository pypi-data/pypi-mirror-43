import json
import logging
import pandas as pd
import numpy as np
import base64
from collections import OrderedDict


class DataFrameIncompleteError(Exception):
  pass


class JobIdGenerator(object):

  _job_id_components = [
      'commit', 'encoder', 'usecase', 'test_suite', 'FPGA', 'build_options',
      'id'
  ]

  def append_job_id_to_dataframe(self, df):
    if not set(self._job_id_components).issubset(df.columns):
      raise DataFrameIncompleteError

    return df.apply(lambda row: pd.concat([row, pd.Series({'job_id': base64.urlsafe_b64encode(json.dumps(row[self._job_id_components].to_dict(OrderedDict)))})]), axis=1)
