import re
import apache_beam as beam


class CleanTweet(beam.DoFn):
    def process(self, element):
        tweet = re.sub(r"http\S+", "", element)  # Remove URLs
        tweet = re.sub(r"RT\s+@\w+", "", tweet)  # Remove 'RT @user'
        tweet = tweet.replace('#', '')  # Remove hashtags
        return [tweet.strip()]
