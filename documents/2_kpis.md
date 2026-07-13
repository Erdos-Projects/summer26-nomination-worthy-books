# KPIs and metrics

When we look at our data, the first thing we notice is that we have a massive class imbalance, as shown in the graphs below.

<img src="../graphics/books_per_year.png" width=500 height=400> <img src="../graphics/percent_nominees.png" width=500 height=400>

This means that if we just predict every book to not be a nominee, we would get >0.9 accuracy score. Additionally, we will need to choose classification models that are less sensitive to such massive class imbalances. 

### Primary metric
Our project is of interest to both sell-side stakeholders, such as publishers and booksellers, who may take our model's predictions into account when making marketing decisions, and buy-side stakeholders, such as readers and authors, who are interested in knowing which books are most likely to be an awards finalist. For each side, they are pulled by different motivations. Sell-side stakeholders, may lose out if they spend a lot of resources on a book that ultimately does not become a finalist, which means that they may be more interested in false positives. The buy-side, however, may be more interested in the rate of true positives. These two notions are captured by precision and recall. In order to balance the competing interests of the two sides, we choose the $F_1$ score as a good compromise between the two. 

### Secondary metrics
Our approache involves the use of LearnToRank models. Such models take in data, and ranks them according to which books the model think are most likely to be awards finalists. Such models are scored based on the **normalized discounted culmulative gain (ndcg)** which is defined in the following way. 

Let $rel_i$ be the graded relevance given to entry $i$ by our ranker model. The **discounted culmulative gain** at rank position $p$ is given by
$$
DCG_p = \sum_{i=1}^p \frac{rel_i}{\log_2 (i + 1)}.
$$
Let $REL_p$ be the list of all books sorted by relevance upto the $p$-th most relevant entry. The *ideal discounted cumulative gain* is defined as
$$
IDCG_p = \sum_{i=1}^{|REL_p|} \frac{2^{rel_i} - 1}{\log_2 (i + 1)}.
$$
The ndcg@k metric is then defined as
$$
NDCG_k = \frac{DCG_k}{IDCG_k}.
$$

As an additional metric, we also used precision@k, the precision of our LearnToRank's top $k$ results against target.

We evaluated our models for $k \in \{5, 10, 15, 20\}$.