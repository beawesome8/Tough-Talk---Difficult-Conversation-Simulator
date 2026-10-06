from fastapi import FastAPI

app = FastAPI(title="Tough Talk")


@app.get("/health")
def health():
    return {"status": "ok"}
