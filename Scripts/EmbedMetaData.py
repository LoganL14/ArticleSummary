""" Create embeddings from downloaded metadata JSON files using Sentence Transformers model. """


from sentence_transformers import SentenceTransformer
from config import EMBED_MODEL, METADATA_ROOT, EMBEDDINGS_ROOT
from context import ctx
from pathlib import Path
import json
import numpy as np

def get_metadata_files(start_utc_time: str) -> list[str]:
    """ Get list of metadata files for a given run date """

    metadata_folder = Path(METADATA_ROOT) / start_utc_time
    return [str(fp) for fp in metadata_folder.glob("*")]

def load_metadata(metadata_file: str) -> dict:
    """ Read the metadata files """

    with open(metadata_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def save_embeddings(texts: str, metadata_file: str) -> None:
    """ Save both embeddings, . /downloaded_embeddings  """
    
    #create directory for files
    out_dir = Path(EMBEDDINGS_ROOT) / ctx.start_utc_time
    out_dir.mkdir(parents=True, exist_ok=True)

    #embedding model
    embeddings = model.encode(texts)

    #create paths
    base = Path(metadata_file).stem  # ex '2512.21078v1'
    vec_path = out_dir / f"{base}_vectors.npy"
    
    #save vectors to path 
    np.save(vec_path, embeddings)
    print(f"[SAVE] Vectors: {vec_path} (shape={embeddings.shape})")



if __name__ == "__main__":

    model = SentenceTransformer(EMBED_MODEL)
    metadata_files = get_metadata_files(ctx.start_utc_time)
    #print(metadata_files)

    for mf in metadata_files:
        try:
            meta = load_metadata(mf)
        except ValueError as e:
            print(f"[WARN] Skipping metadata: {mf}  Error: {e}")
            continue
        texts = json.dumps(meta)
        save_embeddings(texts, mf)
        