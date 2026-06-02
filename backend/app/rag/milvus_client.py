"""
Connexion Milvus et helpers de bas niveau.
Toute la logique RAG métier va dans rag_service.py (J4).
"""
import os
import logging
from pymilvus import connections, utility

logger = logging.getLogger(__name__)

_MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
_MILVUS_PORT = int(os.getenv("MILVUS_PORT", "19530"))


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