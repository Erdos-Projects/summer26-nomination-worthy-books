import numpy as np
import csv
import pandas as pd
import json
import bs4
from bs4 import BeautifulSoup
import requests
import time 
years = np.arange(1953, 2027, step=1) # all years from 1953 to 2026 inclusive

hugo_file = "hugo_nominees.csv"

cols = ["title", "author", 'year']

with open(hugo_file, 'w') as output:
    writer = csv.writer(output)
    writer.writerow(cols)

    for year in years:
        print("Getting {} winners \n".format(year))
        try:
            response = requests.get(url="https://www.sfadb.com/Hugo_Awards_{}".format(year), timeout=10)
            response.raise_for_status()
        except:
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        novel_div = soup.find('div', class_='category', string='Novel')

        if novel_div == None:
            continue

        novel_list = novel_div.find_next_sibling('ul')

        listvals = []

        for item in novel_list:
            novel = item.get_text(strip=True)
            if novel == '':
                continue
            if 'Winner' in novel:
                title = novel.split(':')[-1].split(',')[0]
                author = novel.split(':')[-1].split(',')[1].split('(')[0]
            else:
                title = novel.split(',')[0]
                author = novel.split(',')[1].split('(')[0]
            writer.writerow([title, author, year])
        time.sleep(1) 
