import apache_beam as beam


class MockReadFromTCP(beam.DoFn):
    def process(self, element):
        return ["mocked_tweet"]


class MockFetchCovidStats(beam.DoFn):
    def process(self, element):
        element["total_case_count"] = 123456
        return [element]


class MockSaveToMongoDB(beam.DoFn):
    def process(self, element):
        # Simulate saving to MongoDB
        return [element]
