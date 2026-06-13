import requests
import json
import csv
import pandas as pd
import time
import hardcover_config

API_URL = "https://api.hardcover.app/v1/graphql"
TOKEN = hardcover_config.hardcover_api
batch_size = 50 # request 50 books per query
lag = 1.5 # one request every 1.5 seconds


isfdb_books = pd.read_csv('isfdb_novels_06-06.csv', delimiter=',')
isbns = isfdb_books['isbn'].tolist()

def get_bookinfo(isbns):
    QUERY = """
    query GetDescriptionsByISBN {
    editions(where: {_or: [
        { isbn_10: { _in: """ + json.dumps(isbns) + """ } },
        { isbn_13: { _in: """ + json.dumps(isbns) + """ } }
      ]}
    
    ) {
        isbn_10
        isbn_13
        title
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


hugo_file = "hardcover_bookdetails_v2.csv"

cols = ["batch_num", "isbn", "title", "description", "tags"]

start_batch = 140

isbn_batches = [isbns[i:i+batch_size] for i in range(0, len(isbns), batch_size)]


with open(hugo_file, 'a') as output:
    writer = csv.writer(output, delimiter='\t')

    if start_batch == 0:
        writer.writerow(cols)

    for num_batch, batch in enumerate(isbn_batches[start_batch:], start=start_batch):
        query_results = get_bookinfo(batch)
        for bookedition in query_results:
            original_isbn = None
    
            if bookedition.get("isbn_10") in batch:
                original_isbn = bookedition.get("isbn_10")
            elif bookedition.get("isbn_13") in batch:
                original_isbn = bookedition.get("isbn_13")
            title = bookedition["title"]
            description = bookedition["book"]["description"]
            tags = bookedition["book"]["cached_tags"]
            tag_genres = [{g["tag"]: g["count"]} for g in tags.get("Genre", [])]
            tag_tags = [{g["tag"]: g["count"]} for g in tags.get("Tag", [])]
            tag_mood = [{g["tag"]: g["count"]} for g in tags.get("Mood", [])]
            all_tags = tag_genres + tag_tags + tag_mood
            writer.writerow([num_batch, original_isbn, title, description, all_tags])
        output.flush()
        if num_batch % 10 == 0:
            print("Completed batch {} out of {}.\n".format(num_batch, len(isbn_batches)))
        time.sleep(lag)