import csv
import json

filtered_file = 'openlibrary_works-descriptions.csv'
with open("ol_dump_works_2026-05-31.txt", 'r') as input:
    with open(filtered_file, 'w') as output:
        writer = csv.writer(output)
        writer.writerow(['work_id', 'title', 'description'])
        for line in input:
            full_line = line.strip().split('\t')
            if len(full_line) < 5:
                continue
            try:
                json_entry = json.loads(full_line[4])
            except json.JSONDecodeError:
                continue
            if 'description' not in json_entry:
                continue
            work_id = full_line[1]
            title = json_entry['title']
            description = json_entry['description']
            
            if type(description) is not str:
                description = description['value']
            writer.writerow([work_id, title, description])