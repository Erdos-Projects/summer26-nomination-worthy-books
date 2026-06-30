import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
from pathlib import Path
from skfda import FDataGrid
from skfda.inference.hotelling import hotelling_test_ind

def main():
    BASE_DIR = Path(__file__).resolve().parent

    BASE_DIR = str(BASE_DIR)

    books = pd.read_csv(BASE_DIR + '/../../data/final_book_dataset_cleaned.csv', sep = '\t', 
            dtype = {
                'isbn' : 'str', # do this explicitly to avoide getting a warning by the interpreter
                'author_birthyear' : 'Int64', # we have to explicitly do this to avoid pandas implicitly casting as float
                'title_id' : 'Int64'
            })
    sample = books[(2000 <= books.release_year) & (books.release_year <= 2013)]
    sample = sample.dropna()

    hugo = sample[sample.hugo]
    nonhugo = sample[~(sample.hugo)]

    with open(BASE_DIR + '/transformer.pkl', 'rb') as trans_file:
        transformer = pickle.load(trans_file)


    hugo_embed = transformer.encode(np.array(hugo.book_synopsis))
    nonhugo_embed = transformer.encode(np.array(nonhugo.book_synopsis))

    fda_hugo = FDataGrid(hugo_embed)
    fda_nonhugo = FDataGrid(nonhugo_embed)

    t2, p = hotelling_test_ind(fda_hugo, fda_nonhugo, n_reps = 100_000)
    
    with open('hugo_t2.txt', 'w') as file:
        file.write("Hugo Hotelling T^2 hypothesis testing\n")
        file.write("Permutation testing with 100,000 repetitions\n")
        file.write('T^2 statistic: {}\n'.format(str(t2)))
        file.write('p value: {}'.format(p))

    return




if __name__ == "__main__":
    main()