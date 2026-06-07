import csv
import json

final_file = "openlibrary_reviews.csv"

with open("ol_dump_ratings_2026-05-31.txt", 'r') as input:
    with open(final_file, 'w') as output:
        writer = csv.writer(output)
        writer.writerow(['work_id', 'star_rating', 'date'])
        for line in input:
            full_line = line.strip().split('\t')
            work_id = full_line[0]
            star_rating = full_line[2]
            date = full_line[3]
            writer.writerow([work_id, star_rating, date])