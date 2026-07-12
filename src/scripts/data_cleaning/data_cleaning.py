# %% [markdown]
# This notebook explores and cleans 'final_book_dataset.csv'.
# I specifically:
# - Removed the column index column
# - Turned all entries in title_id into integers
# - Turned all author birthyears into integers
# - Turned all isbns into strings, so hopefully we get less warnings about this column's dtypes
# - I also parsed the raw HTML book_synopsis entries using html2text. Hopefully this results in something better to use

# %%
import numpy as np
import pandas as pd
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]

# %%


final_dataset_path = REPO_ROOT / 'data' / "final_book_dataset.csv"

books = pd.read_csv('final_book_dataset.csv', sep='\t')
books = books[['title_id', 'title', 'author', 'release_year',
       'release_date', 'first_publisher', 'author_birthyear',
       'author_birthplace', 'isbn', 'book_synopsis', 'tags', 'hugo', 'locus']]

# %%
books.title_id = books.title_id.astype('Int64')
books.author_birthyear = books.author_birthyear.astype('Int64')
books.isbn = books.isbn.astype('str')
books.sample(5)

# %%
# Use html2text to parse the descriptions
# Install only once of course
#%pip install -U html2text

# %%
import html2text

def exception_handled_htmlparse(x):
    try:
        return html2text.html2text(x)
    except AttributeError:
        if pd.isnull(x):
            return ''
        print(x)
    return x

# %%
books.book_synopsis = books.book_synopsis.apply(exception_handled_htmlparse)

# %%
# books

# %%
#books.to_csv('final_book_dataset_cleaned.csv', sep='\t', index=False)

# %%
test = pd.read_csv(
    'final_book_dataset_cleaned.csv',
    dtype={
        'isbn' : 'str', # do this explicitly to avoide getting a warning by the interpreter
        'author_birthyear' : 'Int64', # we have to explicitly do this to avoid pandas implicitly casting as float
        'title_id' : 'Int64'
    }, 
    sep='\t'
    )

# %%
test


