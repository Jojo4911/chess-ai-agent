"""
Connexion Milvus et helpers de bas niveau.
Toute la logique RAG métier va dans rag_service.py (J4).
"""
import os
import logging
from pymilvus import connections, utility, DataType, FieldSchema, CollectionSchema, Collection

logger = logging.getLogger(__name__)

_MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
_MILVUS_PORT = int(os.getenv("MILVUS_PORT", "19530"))
_MILVUS_COLLECTION = os.getenv("MILVUS_COLLECTION", "chess_knowledge")


def connect_milvus() -> None:
    """Ouvre la connexion Milvus (alias 'default'). Idempotent."""
    if connections.has_connection("default"):
        return
    connections.connect(
        alias="default",
        host=_MILVUS_HOST,
        port=_MILVUS_PORT,
    )
    logger.info("Milvus connected : %s:%s", _MILVUS_HOST, _MILVUS_PORT)


def is_milvus_healthy() -> bool:
    """Ping rapide pour le healthcheck."""
    try:
        connect_milvus()
        utility.get_server_version()
        return True
    except Exception as exc:  # noqa: BLE001
        logger.warning("Milvus unhealthy : %s", exc)
        return False
    

def create_collection() -> Collection:
    """Crée ou récupère la collection chess_knowledge avec index HNSW cosine. Idempotente."""
    connect_milvus()

    # Idempotence : si la collection existe déjà, on la charge et on la retourne
    if utility.has_collection(_MILVUS_COLLECTION):
        col = Collection(_MILVUS_COLLECTION)
        col.load()
        return col

    # --- Définition des champs ---
    fields = [
        FieldSchema(name="id",        dtype=DataType.INT64,         is_primary=True, auto_id=True),
        FieldSchema(name="text",      dtype=DataType.VARCHAR,        max_length=65535),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR,   dim=1024),
        FieldSchema(name="nom",       dtype=DataType.VARCHAR,        max_length=256),
        FieldSchema(name="eco",       dtype=DataType.VARCHAR,        max_length=16),
        FieldSchema(name="coups",     dtype=DataType.VARCHAR,        max_length=512),
        FieldSchema(name="source",    dtype=DataType.VARCHAR,        max_length=256),
    ]

    # --- Création de la collection ---

    schema = CollectionSchema(fields=fields, description="Chess knowledge base")
    col = Collection(name=_MILVUS_COLLECTION, schema=schema)

    # --- Création de l'index ---
    
    index_params = {
        "metric_type": "COSINE",
        "index_type": "HNSW",
        "params": {"M": 16, "efConstruction": 200},
    }
    col.create_index(field_name="embedding", index_params=index_params)
    col.load()

    logger.info("Collection %s créée et chargée", _MILVUS_COLLECTION)
    return col