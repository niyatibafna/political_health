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
        self.MAX_TWITTER = 500

    def get_credentials(self, cred_filepath):
        config = configparser.RawConfigParser()
        config.read(cred_filepath)
        return config['twitterAuth']['bearer_token']

    def append_object(self, new_results):
        # try:
        if "meta" in new_results and new_results["meta"]["result_count"] != 0:

            self.results["data"].extend(new_results["data"])

            has_users, new_has_users = False, False
            has_places, new_has_places = False, False
            if "includes" in self.results and "users" in self.results["includes"]:
                has_users = True
            if "includes" in new_results and "users" in new_results["includes"]:
                new_has_users = True
            if "includes" in self.results and "places" in self.results["includes"]:
                has_places = True
            if "includes" in new_results and "places" in new_results["includes"]:
                new_has_places = True

            if has_users and new_has_users:
                self.results["includes"]["users"].extend(new_results["includes"]["users"])
            if not has_users and new_has_users:
                self.results["includes"]["users"] = new_results["includes"]["users"]
            if has_places and new_has_places:
                self.results["includes"]["places"].extend(new_results["includes"]["places"])
            if not has_places and new_has_places:
                self.results["includes"]["places"] = new_results["includes"]["places"]

            self.results["meta"]["result_count"] += new_results["meta"]["result_count"]
            assert self.results["meta"]["result_count"] == len(self.results["data"])

        # except:
            # self.save("intermediate_results.json")


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
                "max_results":self.MAX_TWITTER}

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
            if self.results["meta"]["result_count"] > max_results:
                break


    def save(self, filepath):
        #Save returned data to specified filepath (including "data" and "includes" fields)
        try:
            print("Total tweets: {}".format(self.results["meta"]["result_count"]))
        except:
            print("Something weird happened here...")
        with open(filepath, "w", encoding='utf8') as write_file:
            json.dump(self.results, write_file, ensure_ascii = False, indent = 2)
