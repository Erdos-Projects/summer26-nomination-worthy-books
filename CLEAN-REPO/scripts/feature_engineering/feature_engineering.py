import numpy as np
import csv
import pandas as pd
from itertools import islice
import json
import missingno as msno
import matplotlib.pyplot as plt
import sklearn
import sys
sys.path.append("../scripts")
from feature_engineering.tidy_book_tags import *
from feature_engineering.tidy_publisher import *
from feature_engineering.add_author_award_info import *

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]

dataset_file = REPO_ROOT / 'data' / 'final_book_dataset_cleaned.csv'


books = pd.read_csv(dataset_file, sep = '\t',
        dtype={
            'author_birthyear' : 'Int64',
            'title_id' : 'Int64',
            'isbn' : 'str'
        }
    )

## add month of publication column, 00 means only year is known
books['month_of_publication'] =books['release_date'].str[5:7].str.replace('00','Unknown')

## Add age of author at publication
books['Author_Age_at_Publication'] = 'Unknown'
books['Author_Age_at_Publication'] = books['Author_Age_at_Publication'].case_when([(books['author_birthyear'].isna() == False,books['release_year'] - books['author_birthyear'])])

books['Hugo_Awards_Previously'] = (
    books.groupby('author')['hugo'].cumsum() - books['hugo']
)
books['Locus_Awards_Previously'] = (
    books.groupby('author')['locus'].cumsum() - books['locus']
)

## Add column with boolean if author been nominated for Hugo/Locus prior to that date
books['Hugo_Nominee_Before'] = False
books['Hugo_Nominee_Before'] = books['Hugo_Nominee_Before'].case_when([(books['Hugo_Awards_Previously'] > 0,True)])
books['Locus_Nominee_Before'] = False
books['Locus_Nominee_Before'] = books['Locus_Nominee_Before'].case_when([(books['Locus_Awards_Previously'] > 0,True)])

## Add Author Birthplace by country
books = books.assign(author_birthplace_country=books['author_birthplace'].apply(replace_author_birthplace_country))

## Author Birthplace by continent
books = books.assign(author_birthplace_continent=books['author_birthplace'].apply(replace_author_birthplace_continent))


# clean up publishers
books['first_publisher'] = publisher_tidy(books['first_publisher'])

# clean up tags
books['tags'] = clean_filter_tags(books['tags'])

# combine awards into one target column
books['target'] = books['hugo'] | books['locus']

# MISSINGNESS:
# for the sake of this notebook, we shall:
# - omit book synopses, title_id, isbn, release_date (captured in month), author_birthyear, author_birthplace (captured in country and continent)
# - and turn all empty tags into empty string ""

books = books.drop(["title_id", "isbn", "release_date", "author_birthyear", "book_synopsis", "author_birthplace"], axis=1)

books['tags'] = books['tags'].apply(lambda x: '' if isinstance(x, float) else x)

books['Author_Age_at_Publication'] = pd.to_numeric(
    books['Author_Age_at_Publication'], errors='coerce'
)

print('')

books['Total_Awards_Previously'] = books['Hugo_Awards_Previously'] + books['Locus_Awards_Previously']
books['NomineeBefore'] = books['Hugo_Nominee_Before'] | books['Locus_Nominee_Before']

#we also want to add some more author features:

# how many books author has published to date, including this book
books['author_num_books'] = books.groupby('author').cumcount()
books['new_author'] = (books['author_num_books'] == 1)

# how long since this author was last nominated (if none, set to 100)

books['nomination_years'] = books['release_year'].where(books['target'] == 1)
books['last_nomination_year'] = books.groupby('author')['nomination_years'].ffill().groupby(books['author']).shift(1)
books['years_since_last_nomination'] = books['release_year'] - books['last_nomination_year']
books['years_since_last_nomination'] = books['years_since_last_nomination'].fillna(np.nan)

books.drop(columns=['nomination_years', 'last_nomination_year'], inplace=True)

# how many nominees has this publisher had in the past?
books['publisher_historical_nominations'] = books.groupby('first_publisher')['target'].cumsum() - books['target']
books['publisher_cohort_size'] = books.groupby(['release_year', 'first_publisher'])['title'].transform('count')

books['debut_publisher_importance'] = books['new_author'] * books['publisher_historical_nominations']

books['first_publisher'] = combine_publishers(books['first_publisher'], limitnum=300)

numerical_features = ["Total_Awards_Previously", "author_num_books", "years_since_last_nomination", "publisher_historical_nominations", "publisher_cohort_size", 'debut_publisher_importance']

for col in numerical_features:
    books[col] = books[col].astype(float)


## do multilabel binarizer of tags outside preprocessing. 
from sklearn.preprocessing import MultiLabelBinarizer

tag_labeler = MultiLabelBinarizer()
tag_labels = tag_labeler.fit_transform(books['tags'].fillna(''))

# save as dataframe
tag_dataframe = pd.DataFrame(
    tag_labels,
    columns = ["tag_{}".format(tag) for tag in tag_labeler.classes_],
    index=books.index
)

# concatenate to training dataframe
books = pd.concat([books, tag_dataframe], axis=1)


output_file = REPO_ROOT / 'data' / 'books_engineered.csv'


books.to_csv(output_file)