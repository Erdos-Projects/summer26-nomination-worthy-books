import numpy as np
import csv
import pandas as pd
import json
import bs4
from bs4 import BeautifulSoup
import requests
import time 
years = np.arange(1971, 2027, step=1) # all years from 1953 to 2026 inclusive

locus_file = "locus_nominees3.csv"

cols = ["title", "author", 'year']

with open(locus_file, 'w', encoding='utf-8') as output:
    writer = csv.writer(output)
    writer.writerow(cols)

    for year in years:
        print("Getting {} winners \n".format(year))
        try:
            response = requests.get(url="https://www.sfadb.com/Locus_Awards_{}".format(year), timeout=10)
            response.encoding = 'latin-1'  # show the byte just before 'stival'
            response.raise_for_status()

        except:
            continue
        soup = BeautifulSoup(response.text, 'html.parser')

        for award in ['Novel', 'Sf Novel', 'Fantasy Novel']:

            novel_div = soup.find('div', class_='category', string=award)

            if novel_div == None:
                continue

            novel_list = novel_div.find_next_sibling('ol')

            listvals = []

            for item in novel_list:
                novel = item.get_text(strip=True)
                # print(novel)
                if novel == '':
                    continue
                if ('Winner' in novel) or ('tie' in novel):
                    title = novel.split(':')[-1].split(',')[0]
                    author = novel.split(':')[-1].split(',')[1].split('(')[0]
                else:
                    title = novel.split(',')[0]
                    author = novel.split(',')[1].split('(')[0]
                writer.writerow([title, author, year])
            time.sleep(1) 
