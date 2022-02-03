#!/usr/bin/env python3

import json
import os

# CRAWLED_DATA_DIR = "data/crawled"
class TweetReader:

    def __init__(self, path_to_crawled_data):
        self.CRAWLED_DATA_DIR = path_to_crawled_data

    def filter_good(self, tweet, geoid_place_map):
        if " RT " in tweet["text"]:
            return False

        if "geo" in tweet and "place_id" in tweet["geo"]:
            if geoid_place_map[tweet["geo"]["place_id"]] != "IN":
                return False
        else:
            return False

        return True

    def reader(self, years = None, keywords = None):

        if not years:
            raise ValueError("At least 1 year should be provided.")

        id_tweet_map = dict()
        id = 0

        for year in years:
            fpaths = os.listdir("{}/{}".format(self.CRAWLED_DATA_DIR, year))
            # print(fpaths)
            if keywords:
                key_fpaths = ["{}.json".format(keyword) for keyword in keywords if os.path.exists("{}/{}/{}.json".format(self.CRAWLED_DATA_DIR, year, keyword))]
                # print(key_fpaths)
                fpaths = [path for path in fpaths if path in key_fpaths]

            for fpath in fpaths:
                # id = len(id_tweet_map)
                with open("{}/{}/{}".format(self.CRAWLED_DATA_DIR,year,fpath), "r", encoding = "utf-8") as f:
                    crawled_data = json.load(f)

                if "data" not in crawled_data:
                    continue
                try:
                    geoid_place_map = {place_dict["id"]:place_dict["country_code"] for place_dict in crawled_data["includes"]["places"]}
                    # print(len(geoid_place_map))
                except:
                    geoid_place_map = dict()
                    print("Place map not loaded")

                if "IN" not in geoid_place_map.values():
                    continue

                for tweet in crawled_data["data"]:
                    if self.filter_good(tweet, geoid_place_map):
                        id_tweet_map[id] = tweet["text"]
                        id += 1

                print("Read {} from year {}".format(fpath,  year))
                print("Collected data: ", len(id_tweet_map))

        return id_tweet_map


# tr = TweetReader("data/crawled")
# id_tweet_map = tr.reader(range(2010, 2020))
# print(len(id_tweet_map))
