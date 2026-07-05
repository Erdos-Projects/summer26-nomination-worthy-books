import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
import inquirer
import csv


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]

hugo_file = REPO_ROOT / 'data' / 'raw' / 'hugo_nominees.csv'
locus_file = REPO_ROOT / 'data' / 'raw' / 'locus_nominees.csv'
isfdb_hardcover_file = REPO_ROOT / 'data' / 'isfdb-hardcover-combined.csv'

locus = pd.read_csv(locus_file)

hugo = pd.read_csv(hugo_file)

books = pd.read_csv(isfdb_hardcover_file)

hugo.title = hugo.title.apply(lambda x : x.lstrip('“').rstrip('”'))
locus.title = locus.title.apply(lambda x : x.strip('“').strip('”'))


missing_books = REPO_ROOT / 'data' / 'missing_books.csv'

cols = ["title", "author"]

with open(missing_books, 'w') as output:
    writer = csv.writer(output, delimiter='\t')
    writer.writerow(cols)
    for title in hugo.title:
        if len(books.loc[books.title == title]) == 0:
            authors = hugo[hugo.title == title].author.iloc[0].split('&')
            for author in authors:
                question = [
                    inquirer.List('titles',
                    message="What book matches input ({} by {})?".format(title, author),
                    choices=books['title'][books['author'].str.contains(author)].tolist()  + ['None'],
                ),
                ]
                answer = inquirer.prompt(question)['titles']
                if answer == 'None':
                    print("This book is missing from database. Adding it to missing books.")
                    writer.writerow([title, author])
                else:
                    print("Match found!")
                    matched_title = answer
                    # replace title and author in isfdb dataset to match award
                    mask = (books.title == matched_title) & (books['author'].str.contains(author))
                    books.loc[mask, 'title'] = title
                    books.loc[mask, 'author'] = author
    for title in locus.title:
        if len(books.loc[books.title == title]) == 0:
            authors = locus[locus.title == title].author.iloc[0].split('&')
            for author in authors:
                question = [
                    inquirer.List('titles',
                    message="What book matches input ({} by {})?".format(title, author),
                    choices=books['title'][books['author'].str.contains(author)].tolist()  + ['None'],
                ),
                ]
                answer = inquirer.prompt(question)['titles']
                if answer == 'None':
                    print("This book is missing from database. Adding it to missing books.")
                    writer.writerow([title, author])
                else:
                    print("Match found!")
                    matched_title = answer
                    # replace title and author in isfdb dataset to match award
                    books['title'][(books.title == matched_title) & (books['author'].str.contains(author))] = title
                    books['author'][(books.title == matched_title) & (books['author'].str.contains(author))] = author

hugo_mask = books.author.isin(hugo.author) & books.title.isin(hugo.title)
locus_mask = books.author.isin(locus.author) & books.title.isin(locus.title)

books['hugo'] = hugo_mask
books['locus'] = locus_mask

books.to_csv(REPO_ROOT / 'data' / 'isfdb-hardcover-awards.csv')