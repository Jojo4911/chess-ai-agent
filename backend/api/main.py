from fastapi import FastAPI
from app.api.v1.routers.agent_router import router

app = FastAPI(
    title="Chess API",
    version="1.0.0",
)

@app.get("/api/v1/healthcheck")
def healthcheck():
    return {"status": "ok"}

app.include_router(router)