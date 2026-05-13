from fastapi import FastAPI

app = FastAPI(
    title="Chess API",
    version="1.0.0",
)

@app.get("/api/v1/healthcheck")
def healthcheck():
    return {"status": "ok"}