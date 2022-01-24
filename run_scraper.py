#Calls scraper class over different queries

from scraper import *

CRED_FILEPATH = "credentials/credentials.config"
WORDLIST_FPATH = ""
COUNTRY_CODE = "IN"
MAX_RESULTS = 10000

def get_wordlist(filepath):
    with open(filepath, "r") as wl:
        return [word.strip() for word in wl.read().split("\n") if len(word)!=0]

wordlist = get_wordlist(WORDLIST_FPATH)
years = range(2010, 2022, 2)

for q_term in wordlist:
    for year in years:
        scraper = Scraper(CRED_FILEPATH)
        scraper.crawl(q_term, year, year+1, COUNTRY_CODE, MAX_RESULTS)
        scraper.save()
