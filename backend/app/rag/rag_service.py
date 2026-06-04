from app.rag.milvus_client import create_collection
from app.rag.embedder import bge_m3_ef


def search_knowledge(query: str, top_k: int = 3) -> list[dict]:
    """
    Encode la requête avec `encode_queries`, lance une `col.search()` sur le champ embedding.
    Retourne une liste de dictionnaires avec `text` et les métadonnées.
    """
    # 1. Encodage de la requête
    query_embedding = bge_m3_ef.encode_queries([query])["dense"][0]

    # 2. Récupération de la collection existante
    col = create_collection()

    # 3. Recherche vectorielle
    res = col.search(
        data=[query_embedding],
        anns_field="embedding",
        param={"metric_type": "COSINE", "params": {"ef": 64}},
        limit=top_k,
        output_fields=["text", "nom", "eco", "source"],
    )

    # 4. Création de la liste de dictionnaires
    result = []
    for hits in res:
        for hit in hits:
            result.append({
                "nom": hit.get("nom"),
                "eco": hit.get("eco"),
                "text": hit.get("text"),
                "source": hit.get("source"),
            })
    
    return result