import re
import apache_beam as beam


class CleanTweet(beam.DoFn):
    def process(self, tweet):
        print(f"\nInput: {tweet}")
        cleaning_steps = [
            (r"http\S+", ""),  # Remove URLs
            (r"\bRT\s?:\s?", ""),  # Remove 'RT :' and 'RT:'
            (r"#", "")  # Remove hashtags
        ]

        for pattern, replacement in cleaning_steps:
            tweet = re.sub(pattern, replacement, tweet)
        print(f"Output: {tweet}")
        return [tweet.strip()]
