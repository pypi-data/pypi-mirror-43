import pytest
import unittest
import pandas as pd

from vpxhw_db_job_locator.job_id_gen import JobIdGenerator, DataFrameIncompleteError

class JobIdGeneratorTest(unittest.TestCase):

  def setUp(self):
    self.job_id_gen = JobIdGenerator()

    self.input_df = pd.DataFrame([
        {
            'encoder': 'ENCODER',
            'usecase': 'USECASE',
            'commit': 'COMMIT',
            'FPGA': 'FPGA_FLAG',
            'test_suite': 'TESTSUITE',
            'id': 'ID',
            'build_options': 'BUILD_OPTIONS',
        },
    ])

    job_id = 'eyJjb21taXQiOiAiQ09NTUlUIiwgImVuY29kZXIiOiAiRU5DT0RFUiIsICJ1c2VjYXNlIjogIlVTRUNBU0UiLCAidGVzdF9zdWl0ZSI6ICJURVNUU1VJVEUiLCAiRlBHQSI6ICJGUEdBX0ZMQUciLCAiYnVpbGRfb3B0aW9ucyI6ICJCVUlMRF9PUFRJT05TIiwgImlkIjogIklEIn0='

    self.expected_output = pd.DataFrame([
        {
            'encoder': 'ENCODER',
            'usecase': 'USECASE',
            'commit': 'COMMIT',
            'FPGA': 'FPGA_FLAG',
            'test_suite': 'TESTSUITE',
            'id': 'ID',
            'build_options': 'BUILD_OPTIONS',
            'job_id': job_id,
        },
    ])

    self.input_extra_col_df = pd.DataFrame([
        {
            'encoder': 'ENCODER',
            'usecase': 'USECASE',
            'commit': 'COMMIT',
            'FPGA': 'FPGA_FLAG',
            'test_suite': 'TESTSUITE',
            'id': 'ID',
            'build_options': 'BUILD_OPTIONS',
            'extra_column': 'EXTRA_COLUMN_VALUE',
        },
    ])

    self.expected_extra_col_output = pd.DataFrame([
        {
            'encoder': 'ENCODER',
            'usecase': 'USECASE',
            'commit': 'COMMIT',
            'FPGA': 'FPGA_FLAG',
            'test_suite': 'TESTSUITE',
            'id': 'ID',
            'build_options': 'BUILD_OPTIONS',
            'job_id': job_id,
            'extra_column': 'EXTRA_COLUMN_VALUE',
        },
    ])

  @pytest.mark.JobIdGenerator
  def testJobIdGeneratorAppendJobIdColumnToDataFrame(self):
    pd.testing.assert_frame_equal(
        self.job_id_gen.append_job_id_to_dataframe(self.input_df),
        self.expected_output,
        check_like=True)

  @pytest.mark.JobIdGenerator
  def testJobIdGeneratorRaisesErrorIfInputDataFrameIsIncomplete(self):
    input_df = self.input_df.drop('commit', axis=1)
    with self.assertRaises(DataFrameIncompleteError):
      self.job_id_gen.append_job_id_to_dataframe(input_df)

  @pytest.mark.JobIdGenerator
  def testJobIdGeneratorIgnoresExtraColumns(self):
    pd.testing.assert_frame_equal(
        self.job_id_gen.append_job_id_to_dataframe(self.input_extra_col_df),
        self.expected_extra_col_output,
        check_like=True)


if __name__ == '__main__':
  unittest.main()
