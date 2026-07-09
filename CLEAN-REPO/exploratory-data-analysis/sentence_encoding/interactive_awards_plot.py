def main():
    print('Importing libraries...')

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sentence_transformers import SentenceTransformer
    from sklearn.decomposition import PCA
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent


    print('Initializing transformer...')
    transformer = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


    print('reading dataset...')
    books = pd.read_csv(str(BASE_DIR) + '/../../data/final_book_dataset_cleaned.csv', sep = '\t',
        dtype={
            'author_birthyear' : 'Int64',
            'title_id' : 'Int64',
            'isbn' : 'str'
        }
    )


    train_data = books[(2000 <= books.release_year) & (books.release_year <= 2013)]
    train_data.book_synopsis = train_data.book_synopsis.apply(lambda x : '' if pd.isnull(x) else x)

    loop_breaker = False
    award_name = ''
    while not loop_breaker:
        print("Enter which award: 1 = Locus, 2 = Hugo")
        i = input()
        try:
            i = int(i)
            if i == 1:
                award_name = 'locus'
                loop_breaker = True
                break
            elif i == 2:
                award_name = 'hugo'
                loop_breaker = True
                break
            # we did not reach one of the two above states
            print('Did not enter valid option, try again')
            
        except:
            print('Did not enter valid option, try again')
        
    assert(award_name == 'hugo' or award_name == 'locus')

    print('Making interactive plot for', award_name + '...')
        

    award = train_data[train_data[award_name]]
    nonaward = train_data[~(train_data[award_name])]


    print('Embedding synposes...')

    train_embed = transformer.encode(np.array(train_data.book_synopsis))

    award_embed = transformer.encode(np.array(award.book_synopsis))
    nonaward_embed = transformer.encode(np.array(nonaward.book_synopsis))


    print('Getting first 3 components from PCA...')

    pca = PCA(n_components = 3)
    pca.fit(train_embed)

    award3d = pca.transform(award_embed)
    nonaward3d = pca.transform(nonaward_embed)

    award3d = award3d.transpose()
    nonaward3d = nonaward3d.transpose()


    print('Plotting...')

    ax = plt.figure().add_subplot(projection = '3d')

    ax.scatter(award3d[0], award3d[1], award3d[2], color='orange', alpha=1.0)

    ax.scatter(nonaward3d[0], nonaward3d[1], nonaward3d[2], color='blue', alpha=0.01)

    plt.show()
    return

if __name__ == '__main__':
    main()