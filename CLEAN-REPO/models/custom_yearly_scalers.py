import numpy as np
import pandas as pd
import sklearn
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

class YearByYearStandardScaler(BaseEstimator, TransformerMixin):
    def __init__(self, year_column='year', scale_columns=None):
        self.scale_columns = scale_columns
        self.year_column = year_column

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = X.copy()
        # apply standard scaler to each year group by group
        for year, data in X.groupby(by=self.year_column):
            imputer = SimpleImputer(strategy='mean')
            X.loc[data.index, self.scale_columns] = imputer.fit_transform(data[self.scale_columns])

            scaler = StandardScaler()
            # print(X.loc[data.index, 'Locus_Awards_Previously'].mean(), X.loc[data.index, 'Locus_Awards_Previously'].std())
            X.loc[data.index, self.scale_columns] = scaler.fit_transform(data[self.scale_columns])#pd.DataFrame(scaler.fit_transform(data[self.scale_columns]))
            # print(X.loc[data.index, self.scale_columns])
        return X.drop(columns=[self.year_column])
    
    def get_feature_names_out(self, input_features=None):
            if input_features is None:
                raise ValueError("input_features must be provided to get names.")
            input_features = np.asarray(input_features, dtype=object)
            # CONCRETELY: This step drops the year column but preserves all numerical scale columns
            return input_features[input_features != self.year_column]
    
class YearlyGenreTagScaler(BaseEstimator, TransformerMixin):
    def __init__(self, year_column='year', tag_columns=None):
        self.tag_columns = tag_columns
        self.year_column = year_column

    def fit(self, X, y=None):
        self.is_fitted_ = True
        return self

    def transform(self, X, y=None):
        X = X.copy()

        similarity_series = pd.Series(dtype=float, index=X.index)

        for year, data in X.groupby(by=self.year_column):
            tag_data = data[self.tag_columns]
            similarity = cosine_similarity(tag_data)
            book_mean_similarity = np.mean(similarity, axis=0)
            similarity_series.loc[data.index] = book_mean_similarity

        X['cohort_similiarity'] = similarity_series
        return X.drop(columns=self.tag_columns+ [self.year_column])
    
    def get_feature_names_out(self, input_features=None):
            if input_features is None:
                raise ValueError("input_features must be provided to get names.")
            
            # CONCRETELY: This step drops all tag columns and the year column, 
            # and outputs EXACTLY one brand new column name.
            return np.array(['cohort_similiarity'], dtype=object)


class YearlyPastNomineeSimilarityScaler(BaseEstimator, TransformerMixin):
    def __init__(self, year_column='release_year', tag_columns=None):
        self.tag_columns = tag_columns
        self.year_column = year_column

    def fit(self, X, y=None):
        if y is None:
            raise ValueError("This transformer requires a target array `y` to identify historical winners.")
            
        # Temporarily link X and y to find winners across history
        temp_df = X.copy()
        temp_df['is_winner'] = y
        
        # Store a lookup of winner matrices per year as an internal attribute
        self.winner_lookup_ = {}
        for year, group in temp_df[temp_df['is_winner'] == 1].groupby(self.year_column):
            self.winner_lookup_[year] = group[self.tag_columns].values
            
        return self

    def transform(self, X, y=None):
        X = X.copy()
        past_winner_sim_series = pd.Series(dtype=float, index=X.index)
        
        for current_year, data in X.groupby(by=self.year_column):
            past_vectors = [v for yr, v in self.winner_lookup_.items() if yr < current_year]
            
            if not past_vectors:
                past_winner_sim_series.loc[data.index] = 0.0
                continue
                
            past_winners_matrix = np.vstack(past_vectors)
            current_matrix = data[self.tag_columns].values
            
            sim_matrix = cosine_similarity(current_matrix, past_winners_matrix)
            past_winner_sim_series.loc[data.index] = np.mean(sim_matrix, axis=1)

        X['past_winner_similarity'] = past_winner_sim_series
        return X.drop(columns=self.tag_columns + [self.year_column])
    

    def get_feature_names_out(self, input_features=None):
        if input_features is None:
            raise ValueError("input_features must be provided to get names.")
        
        # CONCRETELY: This step drops all tag columns and the year column, 
        # and outputs EXACTLY one brand new column name.
        return np.array(['past_winner_similarity'], dtype=object)
