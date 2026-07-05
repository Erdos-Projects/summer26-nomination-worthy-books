import numpy as np
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
from sklearn.linear_model import LogisticRegression

class CustomClassifier:
    def __init__(self, n_neighbors = 10, weights = 'distance', n_jobs = -1, class_weight = 'balanced'):
        # these should really be private fields
        self.knn = KNeighborsClassifier(n_neighbors = n_neighbors, weights = weights, n_jobs = n_jobs)
        self.log_step = LogisticRegression(class_weight= class_weight)

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

        #print(X)
        #print(X['encoded_synopsis'])

        X_synopsis = X['encoded_synopsis'].explode().values.astype(float).reshape(-1, 384)

        self.knn.fit(X_synopsis, y)

        '''
        self.log_step = Pipeline([
            ('knn step', ColumnTransformer([
                ('pass', 'passthrough', ['num_prev_awards']),
                ('knn step', FunctionTransformer(
                    lambda x : self.knn.predict(x.explode().values.astype(float).reshape(-1, 384))
                ), 'encoded_synopsis')
            ],
            remainder='drop')),
            ('log_reg', LogisticRegression(class_weight = 'balanced'))
        ])'''

        X['knn_pred'] = self.knn.predict(X_synopsis)

        self.log_step.fit(X[['knn_pred', 'num_prev_awards']], y)
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


        return self.log_step.predict(X[['knn_pred', 'num_prev_awards']])
        


