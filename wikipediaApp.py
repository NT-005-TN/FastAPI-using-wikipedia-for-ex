from fastapi import FastAPI
from pydantic import BaseModel
import wikipedia
import uvicorn

app = FastAPI()

# Схемы
class SummaryResponse(BaseModel):
    topic: str
    summary: str

class SearchResponse(BaseModel):
    query: str
    results: list

class TopicRequest(BaseModel):
    topic: str

class TopicResponse(BaseModel):
    title: str
    summary: str
    url: str


# Роут 1: Path параметр - получить краткое описание темы
@app.get("/summary/{topic}", response_model=SummaryResponse)
def get_summary(topic: str):
    return {
        "topic": topic,
        "summary": wikipedia.summary(topic, sentences=20)
    }

# Роут 2: Query параметр - поиск статей
@app.get("/search", response_model=SearchResponse)
def search_wiki(q: str):
    return {
        "query": q,
        "results": wikipedia.search(q, results=25)
    }

# Роут 3: POST с телом - получить данные о статье
@app.post("/topic", response_model=TopicResponse)
def get_topic(data: TopicRequest):
    page = wikipedia.page(data.topic)
    return {
        "title": page.title,
        "summary": wikipedia.summary(data.topic, sentences=2),
        "url": page.url
    }

if __name__ == "__main__":
    uvicorn.run(
        "wikipediaApp:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )