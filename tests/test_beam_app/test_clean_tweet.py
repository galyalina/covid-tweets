import unittest
import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to
from beam_app.clean_tweet import CleanTweet


class CleanTweetTest(unittest.TestCase):
    def test_clean_tweet(self):
        with TestPipeline() as p:
            input_tweets = [
                'RT: This is a tweet about #COVID19 https://example.com',
                'Another random tweet',
                '#StaySafe, stay home!',
                'RT: Important update on the pandemic'
            ]

            expected_output = [
                'This is a tweet about COVID19',
                'Another random tweet',
                'StaySafe, stay home!',
                'Important update on the pandemic'
            ]

            input_collection = p | 'CreateInput' >> beam.Create(input_tweets)
            output_collection = input_collection | 'CleanTweets' >> beam.ParDo(CleanTweet())

            assert_that(output_collection, equal_to(expected_output))


if __name__ == '__main__':
    unittest.main()
