#Calls scraper class over different queries
import os
import time
from scraper import *

CRED_FILEPATH = "credentials/credentials.config"
WORDLIST_FPATH = "wordlists/political_controversies.txt"
COUNTRY_CODE = "IN"
MAX_RESULTS = 5000
OUT_DATA_FPATH = "data/crawled/"

def get_wordlist(filepath):
    with open(filepath, "r") as wl:
        return [word.strip() for word in wl.read().split("\n") if len(word)!=0]


wordlist = get_wordlist(WORDLIST_FPATH)
print("WORDLIST: ", wordlist[:5])

years = list(range(2019, 2021))

scraper = Scraper(CRED_FILEPATH)

for year in years:
    year_dpath = os.path.join(OUT_DATA_FPATH, str(year))
    if not os.path.isdir(year_dpath):
        os.mkdir(year_dpath)
    for q_term in wordlist:
        yq_fpath = os.path.join(year_dpath, q_term.split(" ")[0]+".json")
        #AVOID REPETITIONS
        if os.path.exists(yq_fpath):
            continue
        print("SEARCHING FOR {} in the year {}".format(q_term, year))
        scraper.crawl(q_term, year, year+1, COUNTRY_CODE, MAX_RESULTS)
        scraper.save(yq_fpath)
        # time.sleep(1)
