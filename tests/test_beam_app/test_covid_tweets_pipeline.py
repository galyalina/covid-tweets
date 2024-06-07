import unittest
from unittest.mock import patch
from apache_beam.options.pipeline_options import PipelineOptions
from beam_app.pipeline import CustomPipelineOptions, process_tweets
from tests.mock_transforms import (
    MockReadFromTCP,
    MockFetchCovidStats,
    MockSaveToMongoDB,
)
from apache_beam.testing.test_pipeline import TestPipeline


class CovidTweetsPipelineTest(unittest.TestCase):
    @patch("beam_app.pipeline.ReadFromTCP", new=MockReadFromTCP)
    @patch("beam_app.pipeline.FetchCovidStats", new=MockFetchCovidStats)
    @patch("beam_app.pipeline.SaveToMongoDB", new=MockSaveToMongoDB)
    def test_pipeline_with_parameters(self):
        test_args = [
            "--tcp_host",
            "localhost",
            "--tcp_port",
            "5555",
            "--mongo_uri",
            "mongodb://localhost:27017/test_db",
            "--covid_stats_url",
            "https://example.com/covid_stats",
        ]

        options = PipelineOptions(test_args)
        custom_options = options.view_as(CustomPipelineOptions)

        with TestPipeline(options=options) as p:
            process_tweets(custom_options, p)

            # Collect the output for assertions
            result = p.run()
            result.wait_until_finish()

        # If the pipeline runs without errors, the test passes
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
