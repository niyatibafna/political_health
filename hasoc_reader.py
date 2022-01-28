#!/usr/bin/env python3
import os
import json

class HasocReader:

    def __init__(self, path_to_hasoc_dir):
        self.HASOC_DIR = path_to_hasoc_dir+"/data"

    def read_tweets(self, fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            post = json.load(f)

        hasoc_id_tweet = dict()
        if "tweet_id" in post and "tweet" in post:
            hasoc_id_tweet[post["tweet_id"]] = post["tweet"]

        ass_tweets = post.get("replies", list()) + post.get("comments", list())
        if ass_tweets:
            for r_c in ass_tweets:
                if "tweet_id" in r_c and "tweet" in r_c:
                    hasoc_id_tweet[r_c["tweet_id"]] = r_c["tweet"]

        return hasoc_id_tweet

    def label_mapper(self, label):
        if label == "HOF":
            return 1
        return 0


    def read_labels(self, fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            labels = json.load(f)

        hasoc_id_label = {id:self.label_mapper(label) for id, label in labels.items()}
        return hasoc_id_label



    def reader(self, id_tweet_map = dict(), id_class_map = dict()):

        text_id = max(list(id_tweet_map.keys())) + 1 if id_tweet_map else 0

        for topic_dir in [f for f in os.listdir(self.HASOC_DIR) if os.path.isdir("{}/{}".format(self.HASOC_DIR, f))]:
            for subdir in [f for f in os.listdir("{}/{}".format(self.HASOC_DIR, topic_dir)) if os.path.isdir("{}/{}/{}".format(self.HASOC_DIR, topic_dir, f))]:
                hasoc_id_tweet = self.read_tweets("{}/{}/{}/{}".format(self.HASOC_DIR, topic_dir, subdir, "data.json"))
                hasoc_id_label = self.read_labels("{}/{}/{}/{}".format(self.HASOC_DIR, topic_dir, subdir, "labels.json"))
                for hasoc_id, tweet in hasoc_id_tweet.items():
                    try:
                        id_tweet_map[text_id] = tweet
                        id_class_map[text_id] = hasoc_id_label[hasoc_id]
                        text_id += 1
                    except:
                        print("Label not found!")
                        pass

        return id_tweet_map, id_class_map


# hr = HasocReader("data/hasoc/hi_en_cm")
# a, b = hr.reader()
# print(len(a), len(b))
# print(list(a.items())[:10])
