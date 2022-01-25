#Calls scraper class over different queries
import os
import time
from scraper import *

CRED_FILEPATH = "credentials/credentials.config"
WORDLIST_FPATH = "wordlists/islamic_religious_terms.txt"
COUNTRY_CODE = "IN"
MAX_RESULTS = 500
OUT_DATA_FPATH = "data/crawled/"

def get_wordlist(filepath):
    with open(filepath, "r") as wl:
        return [word.strip() for word in wl.read().split("\n") if len(word)!=0]


wordlist = get_wordlist(WORDLIST_FPATH)
print("WORDLIST: ", wordlist[:5])
wordlist = wordlist[:1]
# print(wordlist)
# wordlist = ["makaan"]
years = list(range(2010, 2023)) # + list(range(2018, 2022))
# years = [2018]
scraper = Scraper(CRED_FILEPATH)

for year in years:
    year_dpath = os.path.join(OUT_DATA_FPATH, str(year))
    if not os.path.isdir(year_dpath):
        os.mkdir(year_dpath)
    for q_term in wordlist:
        print("SEARCHING FOR {} in the year {}".format(q_term, year))
        scraper.crawl(q_term, year, year+1, COUNTRY_CODE, MAX_RESULTS)
        scraper.save(os.path.join(year_dpath, q_term+".json"))
        # time.sleep(1)
