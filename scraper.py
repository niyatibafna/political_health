#Class for interacting with Twitter API, saving retrieved tweets to JSON
import requests
from requests.structures import CaseInsensitiveDict
import configparser

class Scraper:

    URL = "https://api.twitter.com/2/tweets/search/all"

    def __init__(self, cred_filepath):

        self.bearer_token = self.get_credentials(cred_filepath)
        # self.query_exp = query_phrase
        # self.start_year = start_year
        # self.end_year = end_year
        # self.country_code = country_code
        # self.max_results = max_results
        self.results = dict()

    def get_credentials(self, cred_filepath):
        config = configparser.Configparser()
        config.read(cred_filepath)
        return config['twitterAuth']['bearer_token']

    def crawl(self, query_exp, start_year, end_year, country_code, max_results):
        #Crawl and save in self.results
        query = "{} place_country:{}".format(query_exp, country_code)
        start_time = "{}-01-01T00:00:00Z".format(start_year)
        end_time = "{}-01-01T00:00:00Z".format(end_year)

        headers = CaseInsensitiveDict()
        headers['Accept'] = "application/json"
        headers['Authorization'] = "Bearer {}".format(self.bearer_token)

        rule = {"query":query, \
                "start_time":start_time, \
                "end_time":end_time, \
                "expansions":"geo.place_id,author_id", \
                "place.fields":"contained_within,country,country_code,full_name", \
                "user.fields":"created_at,location", \
                "max_results":max_results}

        self.results = requests.get(URL, params=rule, headers=headers)

    def save(self, filepath):
        #Save returned data to specified filepath (including "data" and "includes" fields)
        with open(filepath, "w", encoding='utf8') as write_file:
            json.dump(self.results, write_file, ensure_ascii = False, indent = 2)
