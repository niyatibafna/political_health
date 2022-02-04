#!/usr/bin/env python3
import os
import json
import pandas as pd

class HasocReader:

    def __init__(self, path_to_hasoc_dir):
        # print(path_to_hasoc_dir)
        self.HASOC_DIR_CM = path_to_hasoc_dir + "/hi_en_cm/data"
        # print(os.listdir(self.HASOC_DIR_CM))
        self.HASOC_DIR_EN = path_to_hasoc_dir + "/en"
        self.HASOC_DIR_HI = path_to_hasoc_dir + "/hi"

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



    def cm_reader(self, id_tweet_map = dict(), id_class_map = dict()):

        text_id = max(list(id_tweet_map.keys())) + 1 if id_tweet_map else 0

        only_take_negatives = False
        for topic_dir in [f for f in os.listdir(self.HASOC_DIR_CM) if os.path.isdir("{}/{}".format(self.HASOC_DIR_CM, f))]:
            if topic_dir not in ["casteism", "religious controversies"]: #"religious controversies", "indian politics"
                only_take_negatives = True
            print("Reading: ", topic_dir.upper())
            for subdir in [f for f in os.listdir("{}/{}".format(self.HASOC_DIR_CM, topic_dir)) if os.path.isdir("{}/{}/{}".format(self.HASOC_DIR_CM, topic_dir, f))]:
                hasoc_id_tweet = self.read_tweets("{}/{}/{}/{}".format(self.HASOC_DIR_CM, topic_dir, subdir, "data.json"))
                hasoc_id_label = self.read_labels("{}/{}/{}/{}".format(self.HASOC_DIR_CM, topic_dir, subdir, "labels.json"))
                for hasoc_id, tweet in hasoc_id_tweet.items():
                    if (only_take_negatives and hasoc_id_label[hasoc_id] == 0) or (not only_take_negatives):
                        try:
                            id_tweet_map[text_id] = tweet
                            id_class_map[text_id] = hasoc_id_label[hasoc_id]
                            text_id += 1
                            # if id_class_map[text_id-1] == 1:
                            #     print(tweet)
                        except:
                            print("Label not found!")
                            pass
            only_take_negatives = False

        return id_tweet_map, id_class_map

    def hi_en_reader(self, id_tweet_map = dict(), id_class_map = dict()):

        DIRS = [self.HASOC_DIR_EN, self.HASOC_DIR_HI]
        for DIR in DIRS:
            for fpath in [f for f in os.listdir(DIR) if f.startswith("hasoc")]:
                if len(id_tweet_map) > 8000:
                    break
                # print("{}/{}".format(DIR, fpath))
                data = pd.read_excel("{}/{}".format(DIR, fpath))
                text_id = max(list(id_tweet_map.keys())) + 1 if id_tweet_map else 0
                for idx in range(len(data['text'])):
                    if self.label_mapper(data['task1'][idx]) == 1:
                        continue
                    id_tweet_map[text_id] = data['text'][idx]
                    id_class_map[text_id] = self.label_mapper(data['task1'][idx])
                    text_id += 1


        return id_tweet_map, id_class_map


    def reader(self, id_tweet_map = dict(), id_class_map = dict()):
        id_tweet_map, id_class_map = self.cm_reader(id_tweet_map, id_class_map)
        print("Length of positive examples: {}".format(len([val for val in id_class_map.values() if val == 1])))
        id_tweet_map, id_class_map = self.hi_en_reader(id_tweet_map, id_class_map)

        return id_tweet_map, id_class_map


# hr = HasocReader("data/hasoc/")
# a, b = hr.reader()
# print(len(a), len(b))
# print(list(a.items())[:10])
