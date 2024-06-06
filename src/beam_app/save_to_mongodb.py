from pymongo import MongoClient
import apache_beam as beam


class SaveToMongoDB(beam.DoFn):
    def __init__(self, uri):
        self.uri = uri
        self.client = None

    def start_bundle(self):
        self.client = MongoClient(self.uri)
        self.db = self.client.tweets
        self.collection = self.db.covid_tweets

    def process(self, element):
        self.collection.insert_one(element)

    def finish_bundle(self):
        if self.client:
            self.client.close()
