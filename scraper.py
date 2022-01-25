#Class for interacting with Twitter API, saving retrieved tweets to JSON
import requests
from requests.structures import CaseInsensitiveDict
import configparser
import json
import time
SLEEP_TIME = 2

class Scraper:
    global URL
    URL = "https://api.twitter.com/2/tweets/search/all"

    def __init__(self, cred_filepath):

        self.bearer_token = self.get_credentials(cred_filepath)
        self.results = dict()

    def get_credentials(self, cred_filepath):
        config = configparser.RawConfigParser()
        config.read(cred_filepath)
        return config['twitterAuth']['bearer_token']

    def append_object(self, new_results):
        if "meta" in new_results and new_results["meta"]["result_count"] != 0:
            self.results["data"].extend(new_results["data"])
            self.results["includes"]["users"].extend(new_results["includes"]["users"])
            self.results["includes"]["places"].extend(new_results["includes"]["places"])
            self.results["meta"]["result_count"] += new_results["meta"]["result_count"]

            assert self.results["meta"]["result_count"] == len(self.results["data"])


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

        self.results = requests.get(URL, params=rule, headers=headers).json()
        time.sleep(SLEEP_TIME)

        new_results = self.results
        while "meta" in new_results and "next_token" in new_results["meta"]:
            print("(Paginating) Total tweets: {}".format(self.results["meta"]["result_count"]))
            # print(self.results)
            rule["next_token"] = new_results["meta"]["next_token"]
            # print(rule)
            new_results = requests.get(URL, params=rule, headers=headers).json()
            time.sleep(SLEEP_TIME)
            self.append_object(new_results)
            if self.results["meta"]["result_count"] > 10000:
                break


    def save(self, filepath):
        #Save returned data to specified filepath (including "data" and "includes" fields)
        with open(filepath, "w", encoding='utf8') as write_file:
            json.dump(self.results, write_file, ensure_ascii = False, indent = 2)
