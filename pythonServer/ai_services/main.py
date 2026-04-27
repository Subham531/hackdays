from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommender.api.routes import recommend, places
from recommender.api.routes import recommend, places, ingest   
from recommender.model.similarity import build_place_corpus
import json

app = FastAPI(
    title="Eco Tourism Recommender API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(recommend.router, tags=["Recommendations"])
app.include_router(places.router,    tags=["Places"])
app.include_router(ingest.router,    tags=["Ingestion"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "recommender"}