import requests
from bs4 import BeautifulSoup
import apache_beam as beam


class FetchCovidStats(beam.DoFn):
    def __init__(self, covid_url):
        self.covid_url = covid_url

    def process(self, element):
        response = requests.get(self.covid_url)
        soup = BeautifulSoup(response.content, "html.parser")
        total_cases = (
            soup.find("div", {"class": "maincounter-number"}).get_text().strip()
        )
        element["total_case_count"] = total_cases
        return [element]
