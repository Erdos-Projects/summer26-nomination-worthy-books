from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
from pathlib import Path

DIR = Path(__file__).parent.resolve()
DIR = str(DIR)

import sys

sys.path.append(DIR + '/../') # This should take us to the project parent folder

from scripts.feature_engineering.feature_engineering import tag_dataframe
from custom_yearly_scalers import YearByYearStandardScaler, YearlyGenreTagScaler, YearlyPastNomineeSimilarityScaler
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder, StandardScaler, FunctionTransformer
from sklearn.impute import SimpleImputer

from sklearn.neighbors import KNeighborsClassifier

import xgboost as xgb


def bool_to_int(x):
    '''
    Helper function to stop pickle from yelling at me
    '''
    return x.astype(int)

'''
This is a short and dirty class to get my custom xgb_ranker_with_synopsis model in one class

It requires the data to already be in some prescribed form, so is not very generalizable. Though, maybe that's ok
because this is very specific code, for our very specific project.
'''
class SynopsisXGBRanker:
    def __init__(self):
        self.knn = KNeighborsClassifier(
            n_neighbors = 2, 
            weights = 'distance', 
            n_jobs = -1) # parameters discovered in another notebook
        
        numerical_features = ["Total_Awards_Previously", "Author_Age_at_Publication", "author_num_books", "years_since_last_nomination", "publisher_historical_nominations", "publisher_cohort_size"]
        categorical_features = ["first_publisher", "month_of_publication"]
        mlb_features = ["tags"]
        bool_features = ["new_author"]
        synopsis = ['encoded_synopsis']

        self.features = numerical_features + categorical_features + list(tag_dataframe.columns) + ['release_year'] + bool_features + ['knn_pred']


        # for each categorical feature, create one-hot encoding
        categorical_pipeline = Pipeline(
            steps=[
                ('solve_nans', SimpleImputer(fill_value='Unknown', strategy='constant')),
                ('onehot', OneHotEncoder(handle_unknown='ignore'))
            ] 
        )

        # numerical features: z-score normalization with the rest of the year.
        # turn bool features to int
        # calculate similarities

        feature_preprocessing = ColumnTransformer(
            transformers=[
                ('numerical_scaling', YearByYearStandardScaler(year_column='release_year', scale_columns=numerical_features), numerical_features + ['release_year']),
                ('bool_to_int', FunctionTransformer(bool_to_int, feature_names_out='one-to-one'), bool_features),
                ('onehot', categorical_pipeline, categorical_features),
            ('tag_similarity', YearlyGenreTagScaler(tag_columns=list(tag_dataframe.columns), year_column='release_year'), list(tag_dataframe.columns) + ['release_year']) ,
            ('nominee_,similarity', YearlyPastNomineeSimilarityScaler(tag_columns=list(tag_dataframe.columns), year_column='release_year'), list(tag_dataframe.columns) + ['release_year']),
            ('synopsis', "passthrough", ['knn_pred'])
            ],
            remainder = 'drop'
        )

        self.model = Pipeline(steps=[
            ('preprocess', feature_preprocessing),
            ('xgb_rank', xgb.XGBRanker(
                tree_method="hist",
                objective="rank:ndcg",
                eval_metric="ndcg@60", # because each year has < 60 nominees, we care most about ranking those.
                lambdarank_pair_method="topk",

                lambdarank_num_pair_per_sample=60, 
                
                max_depth=4,                       
                learning_rate=0.05,
                n_estimators=300,                  
                colsample_bytree=0.7,              
                subsample=0.8
            ))
            ])

    
    def fit(self, X, y):
        '''
        X must have the everything in the features column except knn_pred. 
        It must already have a column of 'encoded_synopsis'
        '''

        X_synopsis = X['encoded_synopsis'].explode().values.astype(float).reshape(-1, 384)

        self.knn.fit(X_synopsis, y)

        X['knn_pred'] = self.knn.predict(X_synopsis)


        self.model.fit(
                X,
                y,
                xgb_rank__qid=X['release_year'],
            )

    
    def predict(self, X):
        '''
        X must have everything in the features column except knn_pred. Instead it needs to have an 'encoded_synopsis'
        column.
        '''

        X_synopsis = X['encoded_synopsis'].explode().values.astype(float).reshape(-1, 384)

        X['knn_pred'] = self.knn.predict(X_synopsis)

        return self.model.predict(X)
