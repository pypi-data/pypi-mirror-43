from jinja2 import Template
import requests
from os.path import basename
import urllib
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import pandas_gbq
from google.oauth2 import service_account

from job_id_gen import JobIdGenerator

url_template = """http://go/vpxhw-quality?{{jobIds}}

{% if encoder %}
  Choose {% for e in encoder %}
  {{ e }}{% endfor %}
  in encoder selection box (top one on the left)
{% endif %}
{% if model_name %}
  Pick '{{model_name}}' in tags filter (second one from the top)
{% endif %}
"""

logger = logging.getLogger(__name__)


class DashboardUrl(object):
  def __init__(self, svc_acct_cred):
    super(DashboardUrl, self).__init__()

    self._encoder = []
    self._model_name = None
    self._jobIds = []


    self._credentials = service_account.Credentials.from_service_account_file(
    svc_acct_cred,
)

  def add_latest_job(self, encoder, usecase, test_suite, commit=None, model_name=None):
    self._encoder.append(' '.join((
        encoder,
        usecase,
    )))

    filters = {
        'encoder': encoder,
        'usecase': usecase,
        'test_suite': basename(test_suite),
        'FPGA': '0',
    }

    if commit:
      filters['commit']=commit

    wheres=[
        k + ' = "' + v + '"'
        for (k, v) in filters.items()
    ]

    if model_name:
      wheres.append('user_tags[ORDINAL(ARRAY_LENGTH(user_tags))] = "' +
                          model_name + '"')

    q='''
    SELECT         DISTINCT commit,
        encoder,
        usecase,
        test_suite,
        FPGA,
        ARRAY_TO_STRING(user_tags, ' ') AS build_options,
        id,
        commit_timestamp
    FROM vpxhw.video_quality_data_v7
    WHERE
    '''+' AND '.join(wheres
    )+'''
    ORDER BY commit_timestamp DESC
    '''

    logger.debug(q)

    configuration = {
      'query': {
        "useQueryCache": False
      }
    }
    df=pandas_gbq.read_gbq(q, project_id='google.com:gchips-cloud',
    credentials=self._credentials,
    dialect='standard',
    # configuration=configuration
    )

    if len(df):
      df = JobIdGenerator().append_job_id_to_dataframe(df)
      self._jobIds.append(df.at[0, 'job_id'])


  def get_dashboard_url(self):
    template = Template(url_template)

    jobIdsString = '&'.join(
        ['job=' + urllib.quote_plus(id) for id in self._jobIds])
    return template.render({
        'jobIds': jobIdsString,
        'encoder': self._encoder,
        'model_name': self._model_name
    })
