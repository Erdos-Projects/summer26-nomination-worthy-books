import pandas as pd
import csv
from pathlib import Path

MODELS_DIR = Path(__file__).resolve().parent
REPO_ROOT = MODELS_DIR.parents[0]
print(REPO_ROOT)

dataset_file = REPO_ROOT / 'data' / 'books_engineered.csv'

books = pd.read_csv(dataset_file)

books_tt = books[(books['release_year'] >= 1971) & (books['release_year'] < 2015)]

books_test = books[(books['release_year'] >= 2015)]

train_file = REPO_ROOT / 'data' / 'books_engineered_train.csv'
test_file = REPO_ROOT / 'data' / 'books_engineered_test.csv'

books_tt.to_csv(train_file)
books_test.to_csv(test_file)