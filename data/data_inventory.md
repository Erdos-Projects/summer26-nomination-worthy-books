# Data Inventory

### List of data sources

| Title | Description of contents | Access method | Licensing | 
| ---   | ----------------------- | ------------- | --------- |
| International Speculative Fiction Database (ISFDB) | A community-built database of science-fiction, fantasy and horror books. Contains bibliographic info of the books as well as some user-created subject/genre tags. | Bulk download from June 6, 2026 archive. | Creative Commons License. | 
| Hardcover | A free reading tracking social platform. Used primarily to acquire book descriptions and subject/genre tags for books using ISBNs. | Hardcover API, June 11 2026. See file `get_novel_descriptions.py`.  |  ... |
| Science Fiction Awards Database (SFADB) | Index of science fiction and fantasy awards. Used to acquire list of all finalists for Hugo Award for Best Novel and Locus Awards for Best (Fantasy, Sci-Fi) Novel. | Web scraping using BeautifulSoup, June 11 2026. See files `get_hugo_nominees.py` and `get_locus_nominees.py`. |


### List of data files

| File name | Source | Description |
| --------- | ------ | ----------- |
|`isfdb_novels_06-06.csv` | ISFDB data dump from June 6 2026. | Extracted from data dump using `isfdb_get_novel_details.sql`. Contains details of all first editions of all English-language SFF novels with known title, author name, ISBN, publisher and publication date. |
|`hardcover_bookdetails.csv` | Hardcover API, June 11 2026. | Descriptions and user-created tags for books in `isfdb_novels_06-06.csv` which were available in Hardcover. Use ISBN to match this to novels in `isfdb_novels_06-06.csv`. Note: delimiter is "\t".  |
|`hugo_nominees.csv` | SFADB, June 11 2026. | Lists all novels who were finalists of Hugo Award for Best Novel since its inception in 1954. Contains title, author, and publication date for each. |
|`locus_nominees.csv` | SFADB, June 11 2026. | Lists all novels who were finalists of Locus Award for Best Novel, Locus Award for Best SF Novel, and Locus Award for Best Fantasy Novel since their inception in 1971. Contains title, author, and publication date for each. |