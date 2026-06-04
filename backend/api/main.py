from fastapi import FastAPI
from app.api.v1.routers.agent_router import router
from app.api.v1.routers.chess_router import router as chess_router
from app.rag.milvus_client import is_milvus_healthy

app = FastAPI(
    title="Chess API",
    version="1.0.0",
)

@app.get("/api/v1/healthcheck")
def healthcheck():
    return {"status": "ok","milvus": "ok" if is_milvus_healthy() else "degraded"}

app.include_router(router)
app.include_router(chess_router)