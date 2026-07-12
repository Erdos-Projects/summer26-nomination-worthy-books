# Modeling summary

This notebook summarizes the various attempts we've made to modeling, including models that we believe did not perform well. 

All in all we've attempted the following:
- SVM classifier
- XGB classifier
- XGB ranker
- XGB ranker with encoded synopsis data
- Logistic regression
- Logistic regression with automated tagging features
- Logistic regression with encoded synopsis data
- LightGBM ranker models
- Various ensemble methods on the encoded synopsis data

We will summarize the results of our model testing below.

### SVM models
SVM models of various types were tested with various feature engineering done to compare performance. Using walkforward cross-validation, the mean $F_1$ scores of the various scenarios tested were around $0.3$ and the metrics for this model was worse than XGB classifier across the board, therefore this model was discarded.

### XGB classifier
The mean $F_1$ score of the XGB classifier model using walkforward cross-validation was $0.467$. The $F_1$ score by year during walkforward cross validation is recorded in the following graph.

<img src='graphics/xgbc_cv.png'>

We see that this model performs decently well, though we believe it could be improved.

### XGB ranker
This model's average $F_1$ score across walkforward cross-validation folds was $0.527$. The $F_1$ score across cross validation folds is the following.

<img src="graphics/xgbr_cv.png">

The graph is more chaotic, but tends to do better than XGB classifier. It turns out that this is one of the best performing models, which we choose as one of our final models.

### XGB ranker with encoded synopsis data
This is an modification of the XGB ranker model above with the incorporation of the encoded synopsis data. In this model, we first apply a $k$-nearest neighbor classifier model on the encoded synopsis point cloud, then we plug in the prediction of the KNN model into the XGB ranker model as an extra feature. 

In testing this model, we found that it does not perform very well when we have missing entries, achieving a mean $F_1$ score of only $0.316$ in cross validation. However, once we drop all entries with missing fields during training and testing, we find that model performs much better, achieving a mean $F_1$ score during cross validation of $0.537$. The graph is shown below.

<img src="graphics/synopxgbr_cv.png">

So after dropping all entries with missing fields, we believe this model's performance is good enough to justify being one of our final models.

### Logistic regression
We trained a logistic regression model as a more advanced baseline model to compare our results against. Using cross validation to optimize the threshold, we have the following graph for $F_1$ scores during cross-validation.

<img src="graphics/logreg_cv.png">

### Logistic regression with automated tagging features
Using the same sentence transformer model that we used with 