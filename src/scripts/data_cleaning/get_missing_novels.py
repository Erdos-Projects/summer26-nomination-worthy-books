import requests
import json
import csv
import pandas as pd
import time

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(REPO_ROOT))

from scripts.data_gathering import hardcover_config


missing_books_file = REPO_ROOT / 'data' / 'missing_books.csv'


API_URL = "https://api.hardcover.app/v1/graphql"
TOKEN = hardcover_config.hardcover_api
batch_size = 1 # request 50 books per query
lag = 1.5 # one request every 1.5 seconds


missing_books = pd.read_csv(missing_books_file, delimiter='\t')
titles = missing_books['title'].tolist()
authors = missing_books['author'].tolist()


def get_bookinfo(titles, authors):
    QUERY = """
query GetDescriptionsByTitlesAndAuthors {
  editions(
    where: {
      book: { title: { _in: """ + json.dumps(titles) + """ } }
      contributions: { author: { name: { _in: """ + json.dumps(authors) + """ } } }    
      language: {code2: {_eq: "en"}}
      }
  ) {
    isbn_10
    isbn_13
    title
    release_year
    publisher {
      name
    }
    contributions {
      contribution
      author {
        name
      }
    }
    book {
      description
      title
      rating
      release_year
      cached_tags
    }
    }
    }
    """

    response = requests.post(
        API_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKEN}",
        },
        json={
            "query": QUERY
        }
    )
    response.raise_for_status()
    data = response.json()
    return data["data"]["editions"]


filepath = REPO_ROOT / 'data' / "missing_book_details.csv"

cols = ["batch_num", "isbn", "title", "author", "release_year", "publisher", "description", "tags"]

start_batch = 0

title_batches = [titles[i:i+batch_size] for i in range(0, len(titles), batch_size)]
author_batches = [authors[i:i+batch_size] for i in range(0, len(authors), batch_size)]

with open(filepath, 'w') as output:
    writer = csv.writer(output, delimiter='\t')

    if start_batch == 0:
        writer.writerow(cols)

    for num_batch, batch in enumerate(title_batches[start_batch:], start=start_batch):
        query_results = get_bookinfo(batch, author_batches[num_batch])
        print(query_results)
        for bookedition in query_results:
            original_isbn = bookedition.get("isbn_13") or bookedition.get("isbn_10")
            title = bookedition["title"]

            contributions = bookedition.get("contributions", [])
            authors = [c['author']['name'] for c in contributions if c.get('contribution') is None]
            if not authors:
                authors = [c['author']['name'] for c in contributions]  # fallback if none are null
            author = authors[0] if len(authors) == 1 else ", ".join(authors)
            
            release_year = bookedition["book"]["release_year"]
            description = bookedition["book"]["description"]
            publisher_info = bookedition.get('publisher')
            publisher = publisher_info['name'] if publisher_info else None
            tags = bookedition["book"]["cached_tags"]
            tag_genres = [{g["tag"]: g["count"]} for g in tags.get("Genre", [])]
            tag_tags = [{g["tag"]: g["count"]} for g in tags.get("Tag", [])]
            tag_mood = [{g["tag"]: g["count"]} for g in tags.get("Mood", [])]
            all_tags = tag_genres + tag_tags + tag_mood
            writer.writerow([num_batch, original_isbn, title, author, release_year, publisher, description, all_tags])
        output.flush()
        if num_batch % 10 == 0:
            print("Completed batch {} out of {}.\n".format(num_batch, len(title_batches)))
        time.sleep(lag)