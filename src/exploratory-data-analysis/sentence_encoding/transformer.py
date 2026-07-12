# save the sentence embedding model locally, so we don't have to make a web call everytime to instantiate the model

from sentence_transformers import SentenceTransformer
import pickle
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


transformer = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

with open(str(BASE_DIR) + '/transformer.pkl', 'wb') as file:
    pickle.dump(transformer, file)