# %%
import numpy as np
import csv
import pandas as pd
from itertools import islice
import json
import missingno as msno
import matplotlib.pyplot as plt
from pathlib import Path

# Here we combine and clean up the data sets by adding the Hardcover descriptions and tags.

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]

hardcover_file = REPO_ROOT / 'data' / 'raw' / 'hardcover_bookdetails.csv'
isfdb_file = REPO_ROOT / 'data' / 'raw' / 'isfdb_novels_06-06_with-null-isbn.csv'


isfdb_books = pd.read_csv(isfdb_file, delimiter=',')
hardcover_data = pd.read_csv(hardcover_file, delimiter='\t')

# Combine ISFDB and Hardcover books, using ISBN code to combine.
# 
isfdb_hardcover = pd.merge(isfdb_books, hardcover_data, on='isbn', how="left")


isfdb_hardcover = isfdb_hardcover.drop(['title_y', 'batch_num', 'type'], axis=1) # drop extra or useless cols


# %%
isfdb_hardcover[~(isfdb_hardcover['synopsis'].isna() | isfdb_hardcover['description'].isna())][['synopsis', 'description']]

# %%
# combine ISFDB synopsis and Hardcover description into one col; if both exist, take the longer one

isfdb_hardcover['book_synopsis'] = isfdb_hardcover['synopsis'].combine(isfdb_hardcover['description'], lambda a, b:(
    a if pd.isna(b) else b if pd.isna(a) else a if len(a) > len(b) else b 
))

# %%
# drop extra columns 
isfdb_hardcover = isfdb_hardcover.drop(['synopsis', 'description'], axis=1) # drop extra or useless cols

# %%
# combine book tags. Hardcover also gives the # of times a tag has been applied,
# remove these for now

import ast

def combine_tags(a, b):
    if (pd.isna(a) and pd.isna(b)):
        return np.nan
    elif pd.isna(b):
        return a.split(', ')
    b_dict = ast.literal_eval(b)
    b_keys =  [list(item.keys())[0] for item in b_dict]
    if pd.isna(a):
        return b_keys
    else:
        return a.split(', ') + b_keys

isfdb_hardcover['tags'] = isfdb_hardcover['tags_x'].combine(isfdb_hardcover['tags_y'], combine_tags)

# %%
isfdb_hardcover[['tags', 'tags_x', 'tags_y']].head(3)

# %%
isfdb_hardcover = isfdb_hardcover.drop(['tags_x', 'tags_y'], axis=1) # drop extra or useless cols

# %%
isfdb_hardcover['title'] = isfdb_hardcover['title_x']
isfdb_hardcover = isfdb_hardcover.drop(['title_x'], axis=1) # drop extra or useless cols

# %%


# %%

isfdb_hardcover_filepath = REPO_ROOT / 'data' / 'isfdb-hardcover-combined.csv'

isfdb_hardcover.to_csv(isfdb_hardcover_filepath)


