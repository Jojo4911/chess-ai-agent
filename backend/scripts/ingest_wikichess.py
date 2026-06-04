# --- Imports ---
import logging
import os

from app.rag.chunker import path_to_documents, chunk_documents
from app.rag.milvus_client import create_collection
from app.rag.embedder import embed_texts

logger = logging.getLogger(__name__)

_MILVUS_COLLECTION = os.getenv("MILVUS_COLLECTION", "chess_knowledge")

# --- Fonction d'ingestion ---

def ingest() -> None:
    # 1. Chargement et chunk des documents
    chunks = chunk_documents(documents=path_to_documents())

    # 2. Création ou récupération de la collection
    col = create_collection()

    # 3. Sources déjà présentes dans Milvus
    results = col.query(expr='source != ""', output_fields=["source"])
    existing_sources = {r["source"] for r in results}

    # 4. Filtrage des nouveaux chunks
    new_chunks = [
        c for c in chunks
        if c.metadata.get("source", "") not in existing_sources
    ]

    if not new_chunks:
        logger.info("Rien à ingérer : toutes les sources sont déjà présentes.")
        return

    # 5. Embedding des textes bruts
    texts = [c.page_content for c in new_chunks]
    embeddings = embed_texts(texts)

    # 6. Construction des entités dans l'ordre du schéma (sans id, auto_id=True)
    entities = [
        texts,
        embeddings,
        [c.metadata.get("nom", "")    for c in new_chunks],
        [c.metadata.get("eco", "")    for c in new_chunks],
        [c.metadata.get("coups", "")  for c in new_chunks],
        [c.metadata.get("source", "") for c in new_chunks],
    ]

    col.insert(entities)
    col.flush() # garantit la persistance

    new_sources = {c.metadata.get("source", "") for c in new_chunks}
    logger.info(
        "%d chunks ingérés depuis %d source(s) : %s",
        len(new_chunks),
        len(new_sources),
        new_sources,
    )


# --- Point d'entrée ---


def main() -> None:
    """Exécute le pipeline complet d'ingestion"""
    logging.basicConfig(level=logging.INFO)
    ingest()

if __name__ == "__main__":
    main()