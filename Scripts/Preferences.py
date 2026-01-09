

#Representing file and directory paths
from pathlib import Path
#function formatting, ->
from typing import List
#uses config.py to bring in necessary global arguments
from config import SUMMARY_PROMPTS_ROOT, EMBEDDINGS_ROOT, EMBED_MODEL, METADATA_ROOT
#used for embedding / vector use
import numpy as np
from context import ctx
from sentence_transformers import SentenceTransformer
import json



def get_embed_files(start_utc_time: str) -> List[str]:
    """ Pull the current embeddding files (.npy) """
    embed_folder = Path(EMBEDDINGS_ROOT) / start_utc_time
    return [str(p) for p in embed_folder.glob("*.npy")]


def load_embedding(embed_file: str) -> np.ndarray:
    """ Read the embedding npy files into numpy arrays """
    return np.load(embed_file)

def cosine_similarity(a,b):
    """ Compute cosine similarity between two vectors """
    return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))


def embeddings_similiarity(embed_file: str, my_interest_text: str) -> np.ndarray:
    """ Get the embeddings similarity scores to my interest text """
    
    embeddings = load_embedding(embed_file)
    score = cosine_similarity(my_interest_embed, embeddings)

    return score

def top_1_similarities(scores: List[tuple[str, float]]) -> List[tuple[str, float]]:
    """ Get the top 1 similarity scores """
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return sorted_scores[:1]

def get_article_metadata(embed_file: str) -> str:
    """ Get the article metadata from the embedding file path """
    base = Path(embed_file).stem  # ex '2512.21078v1_vectors'
    article_id = base.replace("_vectors", "")
    metadata_folder = Path(METADATA_ROOT) / ctx.start_utc_time
    metadata_file = metadata_folder / f"{article_id}.json"
    
    with open(metadata_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

if __name__ == "__main__":

    my_interest_text = "Efficient inference and compression of transformer-based large language models, including quantization, pruning, distillation, and decoding speed optimizations."

    model = SentenceTransformer(EMBED_MODEL)
    my_interest_embed = model.encode(my_interest_text)

    embed_files = get_embed_files(ctx.start_utc_time)

    scores = []
    for embed_file in embed_files:
        score = embeddings_similiarity(embed_file, my_interest_text) 
        scores.append((embed_file, score))
    print(scores)
    # top1 = top_1_similarities(scores)  
    # top1embedfiles = [item[0] for item in top1]

    # for ef in top1embedfiles:
    #     metadata = get_article_metadata(ef)
    #     print(f"Metadata: {metadata}")