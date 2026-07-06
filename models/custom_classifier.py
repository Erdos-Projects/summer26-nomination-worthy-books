import numpy as np
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

class CustomClassifier:
    def __init__(self, n_neighbors = 10, weights = 'distance', n_jobs = -1, class_weight = 'balanced'):
        self.class_weight = class_weight
        # Attributes
        self.knn = KNeighborsClassifier(n_neighbors = n_neighbors, weights = weights, n_jobs = n_jobs)
        self.log_step = LogisticRegression(max_iter = 1000, class_weight=self.class_weight)

    def fit(self, X, y):
        '''
        Input:
            X : Needs to be exactly the 'encoded_synopses' and 'num_prev_awards' columns of books DataFrame
                i.e. X = books[['encoded_synopsis', 'num_prev_awards']]
            y : Needs to be exactly the 'target' column of the books DataFrame
                i.e. y = books.target
        Output:
        '''
        # we first do a KNeighborsClassifier on our data's encoded_synopses,
        # then we do a logistic regression with the result and num_prev_awards

        X_synopsis = X['encoded_synopsis'].explode().values.astype(float).reshape(-1, 384)

        self.knn.fit(X_synopsis, y)

        X['knn_pred'] = self.knn.predict(X_synopsis)


        self.log_step = Pipeline(
            steps = [
                ('encode birthplace and publisher', ColumnTransformer([
                    #('passthrough', 'passthrough', ['knn_pred', 'num_prev_awards', 'Author_Age_at_Publication']),
                    ('passthrough', 'passthrough', ['knn_pred', 'Hugo_Awards_Previously', 'Locus_Awards_Previously', 'Author_Age_at_Publication']),
                    ('encode', OneHotEncoder(handle_unknown='ignore'), ['first_publisher', 'author_birthplace_country'])
                ])
                ),
                ('log_reg', LogisticRegression(max_iter = 1000, class_weight = self.class_weight))
            ]
        )    

        #self.log_step.fit(X[['knn_pred', 'num_prev_awards', 'first_publisher', 'author_birthplace_country', 'Author_Age_at_Publication']], y)
        self.log_step.fit(X[['knn_pred', 'Hugo_Awards_Previously', 'Locus_Awards_Previously', 'first_publisher', 'author_birthplace_country', 'Author_Age_at_Publication']], y)

        return

    def predict(self, X):
        '''
        Input:
            X : Needs to be exactly the 'encoded_synopses' and 'num_prev_awards' columns of books DataFrame
                i.e. X = books[['encoded_synopsis', 'num_prev_awards']]
            y : Needs to be exactly the 'target' column of the books DataFrame
                i.e. y = books.target
        Output:
        '''

        X_synopsis = X['encoded_synopsis'].explode().values.astype(float).reshape(-1, 384)
        X['knn_pred'] = self.knn.predict(X_synopsis)

        #return self.log_step.predict(X[['knn_pred', 'num_prev_awards', 'first_publisher', 'author_birthplace_country', 'Author_Age_at_Publication']])
        return self.log_step.predict(X[['knn_pred', 'Hugo_Awards_Previously', 'Locus_Awards_Previously', 'first_publisher', 'author_birthplace_country', 'Author_Age_at_Publication']])
         
        



class CustomBaggingClassifier:
    def __init__(self, base_estimator = CustomClassifier, n_estimators = 10, kwargs = {}):
        '''
        (Mostly) copied from the ensemble_i problem session
        Parameters:
            base_estimator: Our CustomClassifier class
            n_estimators: Number of estimators in the ensemble
            kwargs: A dictionary of keyword arguments to pass to our base_estimator
        Attributes:
            self.estimators: A list of instantiated base estimators
        '''

        self.kwargs = kwargs
        self.n_estimators = n_estimators
        self.estimators = [base_estimator(**kwargs) for _ in range(n_estimators)]
    
    def fit(self, X, y):
        '''
        Inputs:
            X: DataFrame that is specified with the same columns as taken in by our CustomClassifier
            y: Target of Hugo | Locus award nominees
        '''
        rng = np.random.default_rng()
        n_samples = X.shape[0]

        for estimator in self.estimators:
            indices = rng.choice(n_samples, n_samples, replace = True)
            X_boot = X.iloc[indices]
            y_boot = y.iloc[indices]

            estimator.fit(X_boot, y_boot)
        return
    
    def predict(self, X):
        '''
        Inputs:
            X: Dataframe of books with encoded_synopsis and num_prev_awards columns
        '''
        preds = np.array([estimator.predict(X) for estimator in self.estimators])
        preds = preds.T
        preds = np.array([
            bool(np.argmax(np.bincount(preds[i]))) for i in range(len(preds))
        ])

        return preds