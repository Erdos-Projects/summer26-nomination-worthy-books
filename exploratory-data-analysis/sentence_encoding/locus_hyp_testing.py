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

    locus = sample[sample.locus]
    nonlocus = sample[~(sample.locus)]

    with open(BASE_DIR + '/transformer.pkl', 'rb') as trans_file:
        transformer = pickle.load(trans_file)


    locus_embed = transformer.encode(np.array(locus.book_synopsis))
    nonlocus_embed = transformer.encode(np.array(nonlocus.book_synopsis))

    fda_locus = FDataGrid(locus_embed)
    fda_nonlocus = FDataGrid(nonlocus_embed)

    t2, p = hotelling_test_ind(fda_locus, fda_nonlocus, n_reps = 100_000)
    
    with open('locus_t2.txt', 'w') as file:
        file.write("Locus Hotelling T^2 hypothesis testing\n")
        file.write("Permutation testing with 100,000 repetitions\n")
        file.write('T^2 statistic: {}\n'.format(str(t2)))
        file.write('p value: {}\n'.format(p))

    return




if __name__ == "__main__":
    main()