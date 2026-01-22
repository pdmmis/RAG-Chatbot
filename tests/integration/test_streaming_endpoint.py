from fastapi.testclient import TestClient
from backend.main import app
def test_streaming_returns_multiple_chunks():
    client = TestClient(app)
    response = client.get("/chat/stream")
    chunks =list(response.iter_text())
    assert len(chunks)>1