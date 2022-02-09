#!/usr/bin/env python3
import json

with open("results/overview/islamic_religious_terms_2010-2020.json", "r") as f:
    ist_overview = json.load(f)
with open("results/overview/political_controversies_2019-2020.json", "r") as f:
    pc_overview = json.load(f)

ist_total = sum([ist_overview[year][key]["Total tweets"] for year in ist_overview for key in ist_overview[year]])
ist_hate = sum([ist_overview[year][key]["Number of hate tweets"] for year in ist_overview for key in ist_overview[year]])
print(ist_total, ist_hate)
print("IST: ", ist_hate/ist_total)

pc_total = sum([pc_overview[year][key]["Total tweets"] for year in pc_overview for key in pc_overview[year]])
pc_hate = sum([pc_overview[year][key]["Number of hate tweets"] for year in pc_overview for key in pc_overview[year]])
print(pc_total, pc_hate)
print("PC: ", pc_hate/pc_total)
