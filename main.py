import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from database import db, create_document, get_documents

app = FastAPI(title="B2B Streaming Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "B2B Streaming Platform Backend is running"}

# Public showcase endpoints

@app.get("/api/channels")
def list_channels(limit: int = 12):
    try:
        items = get_documents("channel", {}, limit)
    except Exception:
        items = []
    # Serialize ObjectId if present
    normalized = []
    for it in items:
        if isinstance(it, dict) and "_id" in it:
            it = {**it, "id": str(it.get("_id"))}
            it.pop("_id", None)
        normalized.append(it)
    return {"channels": normalized}

class DemoRequestPayload(BaseModel):
    company: str
    contact_name: str
    email: str
    use_case: Optional[str] = None
    audience_size: Optional[str] = None
    notes: Optional[str] = None

@app.post("/api/request-demo")
def request_demo(payload: DemoRequestPayload):
    try:
        doc_id = create_document("demorequest", payload.model_dump())
        return {"status": "ok", "id": doc_id}
    except Exception:
        # Fallback when DB is not configured
        return {"status": "ok", "id": "demo"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
