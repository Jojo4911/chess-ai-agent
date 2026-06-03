# --- Imports ---
import os
from dotenv import load_dotenv
from pymilvus import model

load_dotenv()

# --- Configuration ---

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "1024"))

bge_m3_ef = model.hybrid.BGEM3EmbeddingFunction(
        model_name=EMBEDDING_MODEL,
        device='cpu',
        use_fp16=False,
    )

# Le modèle choisi est BGE-M3 car c'est un modèle multilingue, qui peut faire des recherches denses (dense) ou éparses (sparse),
# il est open source et de dimension 1024.

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Construit un index à partir d'une liste de chaînes de caractères brutes.
    """
    docs_embeddings = bge_m3_ef.encode_documents(texts)

    return docs_embeddings["dense"]