# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]

missing_file = REPO_ROOT / 'data' / "missing_books.csv"
missing_finalists_file = REPO_ROOT / 'data' / "missing_book_details.csv"
hugo_file = REPO_ROOT / 'data' / 'raw' / 'hugo_nominees.csv'
locus_file = REPO_ROOT / 'data' / 'raw' / 'locus_nominees.csv'

# %%
missing_list = pd.read_csv(missing_file, delimiter='\t')

# %%
missing_finalists = pd.read_csv(missing_finalists_file, delimiter='\t')

# there are duplicates we wish to remove 

# %%
locus = pd.read_csv(locus_file)
hugo = pd.read_csv(hugo_file)
hugo_mask = missing_finalists.author.isin(hugo.author) & missing_finalists.title.isin(hugo.title)
locus_mask = missing_finalists.author.isin(locus.author) & missing_finalists.title.isin(locus.title)

missing_finalists['hugo'] = hugo_mask
missing_finalists['locus'] = locus_mask

# %%
# get rid of any accidental non-matches

missing_finalists = missing_finalists[~((missing_finalists['hugo'] == False) & (missing_finalists['locus'] == False))]

# %%
# de-duplicate editions, taking the first published 
missing_finalists = missing_finalists.drop_duplicates(['title', 'author'], keep='first')

# %%
missing_finalists.head(5)

# %%
import ast 
def get_tags(b):
    if pd.isna(b):
        return np.nan
    b_dict = ast.literal_eval(b)
    b_keys =  [list(item.keys())[0] for item in b_dict]
    return b_keys
    

missing_finalists['tags'] = missing_finalists['tags'].apply(get_tags)

# %%
missing_finalists['first_publisher'] = missing_finalists['publisher']
missing_finalists['isbn'].apply(lambda x: np.nan if np.isnan(x) else str(x) )
missing_finalists['release_year'].apply(lambda x: np.nan if np.isnan(x) else int(x) )
missing_finalists['book_synopsis'] = missing_finalists['description']


# %%
missing_finalists = missing_finalists.drop(['batch_num', 'description', 'publisher'], axis=1)

# %%

# %%

isfdb_hardcover_filepath = REPO_ROOT / 'data' / 'isfdb-hardcover-awards.csv'

previous_dataset = pd.read_csv(isfdb_hardcover_filepath)

# %%

# %%
# drop duplicates, save all authors when each duplicate is due to different author 
duplicates = previous_dataset[previous_dataset['title_id'].duplicated(keep=False)].sort_values(by='title_id')

for title_id in duplicates['title_id'].tolist():
    duplicatebooks = duplicates[duplicates['title_id'] == title_id]
    authors = duplicatebooks['author'].tolist()
    unique_authors = list(set(authors))
    if len(unique_authors) == 0:
        authorlist = unique_authors[0]
    else:
        authorlist = ', '.join(unique_authors)
    previous_dataset.loc[previous_dataset['title_id'] == title_id, 'author'] = authorlist

# %%
# drop duplicates
previous_dataset = previous_dataset.drop_duplicates('title_id', keep='first', ignore_index=True)

# %%
previous_dataset[previous_dataset['title_id'].duplicated(keep=False)].sort_values(by='title_id')


# %%
full_dataset = pd.concat([previous_dataset, missing_finalists], ignore_index=True)

# %%
# get rid of old index columns

full_dataset = full_dataset.drop(['Unnamed: 0.1', 'Unnamed: 0'], axis=1)

# %%

# %%
# reordering columns a bit
full_dataset = full_dataset[['title_id', 'title', 'author', 'release_year', 'release_date', 'first_publisher',
       'author_birthyear', 'author_birthplace', 'isbn', 
       'book_synopsis', 'tags',  'hugo', 'locus']]

# %%
# want to make sure there are no duplicates

# %%
full_dataset = full_dataset.sort_values(by='release_year').drop_duplicates(['title', 'author'], keep='first')

# %%

# %%
final_dataset_path = REPO_ROOT / 'data' / "final_book_dataset.csv"
full_dataset.to_csv(final_dataset_path, sep='\t')

# %%



