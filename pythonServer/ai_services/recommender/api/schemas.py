from pydantic import BaseModel, Field

class RecommendRequest(BaseModel):
    query: str = Field(..., min_length=2, example="historical heritage tour")
    state: str | None = Field(None, example="Assam") 
    budget: int | None = Field(None, ge=0, example=2000)
    month: str | None = Field(None, example="Dec")
    types: list[str] | None = Field(None, example=["cultural", "historical"])
    top_k: int = Field(5, ge=1, le=20)

class PlaceResult(BaseModel):
    place_id: str
    name: str
    types: list[str]
    activities: list[str]
    description: str
    budget_min: int
    budget_max: int
    best_months: list[str]
    state: str | None = None
    eco_score: float
    popularity: float
    similarity: float
    final_score: float

class RecommendResponse(BaseModel):
    query: str
    intent: str | None
    results: list[PlaceResult]