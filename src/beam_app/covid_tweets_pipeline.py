import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from datetime import datetime
from beam_app.clean_tweet import CleanTweet
from beam_app.fetch_covid_stats import FetchCovidStats
from beam_app.save_to_mongodb import SaveToMongoDB
from beam_app.read_from_tcp import ReadFromTCP
import logging


class CustomPipelineOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument('--tcp_host', type=str, help='Host for the TCP stream')
        parser.add_value_provider_argument('--tcp_port', type=int, help='Port for the TCP stream')
        parser.add_value_provider_argument('--mongo_uri', type=str, help='MongoDB URI')
        parser.add_value_provider_argument('--covid_stats_url', type=str, help='URL to fetch COVID-19 stats')


def process_tweets(custom_options, pipeline):
    mongo_uri = custom_options.mongo_uri.get()
    covid_url = custom_options.covid_stats_url.get()
    tcp_host = custom_options.tcp_host.get()
    tcp_port = custom_options.tcp_port.get()

    (pipeline
     | 'Start' >> beam.Create([None])
     | 'Read Tweets' >> beam.ParDo(ReadFromTCP(tcp_host, tcp_port))
     | 'Clean Tweets' >> beam.ParDo(CleanTweet())
     | 'GroupIntoBatches' >> beam.BatchElements(min_batch_size=20, max_batch_size=20)
     | 'Add Timestamp' >> beam.Map(lambda batch: {'tweets': batch, 'timestamp': datetime.now().isoformat()})
     | 'Fetch COVID Stats' >> beam.ParDo(FetchCovidStats(covid_url))
     | 'Save to MongoDB' >> beam.ParDo(SaveToMongoDB(mongo_uri))
     )


def run(pipeline_options):
    custom_options = pipeline_options.view_as(CustomPipelineOptions)

    with beam.Pipeline(options=pipeline_options) as p:
        process_tweets(custom_options, p)


if __name__ == '__main__':
    logging.getLogger(__name__).setLevel(logging.INFO)
    logging.info("Pipeline stated")
    pipeline_options = PipelineOptions()
    run(pipeline_options)
