import joblib
from pathlib import Path
import pandas as pd
import numpy as np
import sys

DIR = Path(__file__).parent.resolve()
DIR = str(DIR)

sys.path.append(DIR + '/../')

from scripts.feature_engineering.feature_engineering import tag_dataframe
from scripts.feature_engineering.tagging_system import automate_tagging as at
from xgb_ranker_with_synopses_model import SynopsisXGBRanker


'''
This script saves the model from xgb_ranker_with_synopses.ipynb after training with the full training datset.

The model will be dumped as a pickle file in the folder models/trained_models
'''
def main():
    DIR = Path(__file__).parent.resolve()
    DIR = str(DIR) # this gives us the models folder


    transformer = at.load_transformer()


    books_train = pd.read_csv(DIR + '/../data/books_engineered_train.csv')

    # load in data with book_synopsis
    books = pd.read_csv(DIR + '/../data/data_with_author_and_awards.csv',
    dtype = {
        'isbn' : 'str', # do this explicitly to avoide getting a warning by the interpreter
        'author_birthyear' : 'Int64', # we have to explicitly do this to avoid pandas implicitly casting as float
        'title_id' : 'Int64'
    },
    )

    books = books[(1971 <= books.release_year) & (books.release_year <= 2014)]

    books_train = pd.merge(books_train, books[['title', 'author', 'book_synopsis']], on = ['title', 'author'])

    books_train = at.encode_books(books_train, transformer)

    model = SynopsisXGBRanker()

    y = books_train.target

    model.fit(books_train, y)

    file_name = DIR + '/trained_models/xgbranker_with_synopsis_model.pkl'

    joblib.dump(value = model, filename = file_name)

    return

if __name__ == "__main__":
    main()