from sentence_transformers import SentenceTransformer, util
import torch

_model = SentenceTransformer("all-MiniLM-L6-v2")  

def build_place_corpus(places: list[dict]) -> torch.Tensor:
    texts = [place["combined_text"] for place in places]
    return _model.encode(texts, convert_to_tensor=True)

def compute_similarity(user_query: str, place_embeddings: torch.Tensor) -> list[float]:
    query_embedding = _model.encode(user_query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, place_embeddings)[0]
    return scores.tolist()