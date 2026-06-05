# Project Checkpoint 1: Problem Definition, Data Gathering, KPIs

## Problem Definition
This project aims to predict the finalists, i.e. shortlisted nominees, of annual fantasy and science fiction book awards, from the complete list of eligible novels.

We focus on book awards which rely on votes from the fanbase, which are a proxy for popular acclaim within the genre.


### Stakeholders:
…

### Scope: 
We focus on novels eligible to the following awards:
- **Hugo Award for Best Novel**: 
    - Awarded for a story of >40,000 words, eligible only in their first year of publication in English in the United States.
    - Nominations are through fan voting, with the top 6 most nominated novels being the finalists (our prediction target). 
    - These awards have been awarded since 1955 (with retroactive Hugo awards awarded for novels back to 1939. Should we use those?)
    - *note: there are some other award categories for the Hugo, see https://www.thehugoawards.org/hugo-categories/, do any of those also sound interesting?*
- **Nebula Award for Best Novel** 
    - Awarded for a story of >40,000 words, eligible only in their first year of publication in English in the United States. 
    - Nominations are through fan voting, with the top 6 most nominated novels being the finalists (our prediction target). 
    - These awards have been awarded since 1965.
    - *Just like the Hugos there are other categories: https://nebulas.sfwa.org/search-awards/*
- **Locus Award for Best Novel**?
- **Arthur C. Clarke Award for Best Novel**?
    - This award, unlike the others above, is awarded by a committee rather than by fan vote. Would using it confuse the models, or would it be an interesting comparison point?
- **Anti-goals**: We do not focus on commercial success of these novels which might be probed through sales data. 
-
## Data Gathering
### Source Identification
- OpenLibrary: bulk downloads (https://openlibrary.org/developers/dumps)
    - Includes: book metadata, book description, user star ratings, “subjects”/topics 
    - Fairly straightforward to use SQL or such to filter the books to get a dataset of fantasy novel nominees for each given year, I think.
- Possibly Wikidata? For more author data?
- Similarly, Google Books also contains book descriptions and metadata, to fill in anything that is missing. (https://developers.google.com/books) 
- I initially had thought of using Goodreads or TheStorygraph and web scraping their public ratings and review counts for books, as a metric for popularity. However both are explicitly against such use, so we can't really do this ethically. At least OpenLibrary's ratings are accessible, but there are fewer of them. 
    - Some Goodreads book datasets exist on Kaggle but they are not comprehensive, I think?
- In terms of doing some sort of sentiment analysis to capture the "buzz"/"popularity" of books, is it possible to use some other social media sources that do allow their data to be used for non-commercial ML training use? Perhaps Reddit's fantasy subdreddit? Or SFF magazines?

### Acquisition strategy
- OpenLibrary: their latest bulk download (dated May 31) https://openlibrary.org/developers/dumps
- ... fill in more...

### Ethical and legal considerations
- ...

## Data Assessment & Assessing Learnability
... Some of this will have to come after we look into data cleaning?

## KPI Definition (Key Performance Indicators)

### Primary KPI
...
### Secondary KPI
...
### Baseline definition
...