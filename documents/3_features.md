# Model Features

Here we describe the features of the novels in our dataset - both those included in the dataset and those engineered therefrom. We discuss which we have retained for model training, and which we have omitted through data exploration.

### Existing Features

From the raw datasets from ISFDB, supplemented from SFADB and Hardcover, we have the following information for each novel entry:

| Category | Features | 
| -------- | -------- |
| Publication information | Title, release year, release date, first publisher, ISBN | 
| Author information | Birth year, birthplace | 
| Book description | synopsis, user-added tags | 

Certain of these data points do not hold useful information, namely the title and ISBN of the novel, and were removed from the dataset.

### Feature Engineering

Many of these features are not usable in their raw state: we use them to determine more useful features as described below. Throughout this process, we avoid time leakage by only considering events prior to a novel's publication.

| Original Feature | Engineered feature(s) | Script (in ```src/scripts/feature_engineering``` unless otherwise specified) | 
| ----------------  | -------------------- | ---------------------------- |
| Author name | Previous nominee flag (true/false) at time of publication. Number of Hugo / Locus award nominations for other novels, prior to publication. Number of other books published prior to publication.| ```add_author_award_info.py``` |
| Author birth year | Author age at the time of publication. | ```add_author_award_info.py``` |
| Author birthplace | Author country of birth,  and continent of birth (simplified from the original dataset to combine duplicate entries, e.g. NZ -> New Zealand). | ```add_author_award_info.py```. | 
| Publisher | Simplified to combine duplicate entries (e.g. Tor Books -> Tor), and combining publishers with fewer than a threshold number of publications to 'Other'. | ```tidy_publisher.py```. |
| Release date | Month of publication if known, otherwise 'Unknown'. | ```add_author_award_info.py``` |
| User-added genre tags | Cleaned up tags: removing metadata tags (e.g. "to-read" tag), data leakage tags (e.g. "top-100-books", "hugo-winner"). Simplifying tags using  ```nltk``` to lemmatize to word stems (combining e.g. adventurous, adventure), and combining same tags (e.g. sci-fi, sf) and like tags under umbrella terms (e.g. disaster, epidemic -> apocalypse) to decrease number of tags. Simplified tags used as a vector space using ```multi-label binarizer```, then to calculate the cosine similarity between tags in books in the same year (cohort similarity) and between a book and previous nominees (past-nominee similarity). | ```tidy_tags.py``` |
| Synopses | Encoded as vectors using the pretrained model all-MiniLM-L6-v2. | ```tagging_system``` folder. |
| Synopses & user-added genre tags | Used to generate an "auto-tagging" system to create tags based on similarities with other tagged books. | See ```src/exploratory-data-analysis/sentence_encoding``` folder. |

### Retained and dropped features

Through EDA, we elected to keep certain features while dropping others from our models.

We found that author past-nomination information was very important across models, especially XGB models. Models also relied on cohort similarity and past-nominee similarity -- the Logistic Regression model in particular relied most on past-nominee similarity (a positive predictor for nomination) and cohort similarity (negatively correlated with nomination). We also retained publisher information, as our EDA revealed that certain large publishers were over-represented in the nomination pool. Month of publication was also retained.

The encoded book synopses, as well as the encoded auto-tags, were retained, in order to compare models' performance with and without these NLP encodings.

We found that author age at time of publication did not add supplemental information, compared to author past nominations and number of books published, and thus we dropped this feature. Additionally, author birthplace was dropped as model performance was not improved by including it -- and due to the fact that most authors in this dataset were born in the United States.

We summarize our retained features below.

|                     | Features                                                                        | Processing                                                      |
| ---------------------| ---------------------------------------------------------------------------------| -----------------------------------------------------------------|
| Author metrics      | previously nominated (boolean feature), past nomination count, past novel count | z-score normalization compared to year cohort                   |
| Publisher prestige  | past nomination count, cohort size (number of books published that year)        | z-score normalization compared to year cohort                   |
| Publication details | First publisher, publication month                                              | One-hot encoding                                                |
| Genre similarity    | Cohort similarity, past-nominee similarity                                      | Cosine similarity in tag vector space                           |
| Book synopsis data  | Text of book description/synopsis from databases                                | Encoded as vectors using the pretrained model all-MiniLM-L6-v2. |
