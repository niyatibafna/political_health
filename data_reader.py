import json
import os

# CRAWLED_DATA_DIR = "data/crawled"
class TweetReader:

    def __init__(self, path_to_crawled_data):
        self.CRAWLED_DATA_DIR = path_to_crawled_data

    def filter_good(self, text):
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

                for tweet in crawled_data["data"]:
                    if self.filter_good(tweet["text"]):
                        id_tweet_map[id] = tweet["text"]
                        id += 1


        return id_tweet_map


# tr = TweetReader()
# id_tweet_map = tr.reader([2010, 2011],["halal"])
# print(len(id_tweet_map))
