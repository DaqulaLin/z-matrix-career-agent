# Filename: main.py
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google.cloud import firestore
from agent import run_compass_engine

# Initialize a clean FastAPI engine
app = FastAPI(title="Compass Oracle API")

# Initialize Firestore Client
db = None
try:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "spatial-cargo-484310-t2")
    db = firestore.Client(project=project_id, database="democompass")
    print(f"[Init] Successfully initialized Firestore client for database 'democompass'")
except Exception as e:
    print(f"[Init Warning] Failed to initialize Firestore: {str(e)}")

# Define strict input parameter validation
class CompassRequest(BaseModel):
    target_job: str
    mode: str = "mixed"  # Defaults to mixed mode

# Core compass deduction interface (handles POST requests)
@app.post("/compass")
def generate_compass(req: CompassRequest):
    try:
        print(f"[Compass] Received deduction request: job={req.target_job}, mode={req.mode}")
        
        # 1. Generate canonical cache key
        job_key = req.target_job.strip().lower()
        doc_id = f"{job_key}_{req.mode}"
        doc_ref = db.collection("job_deductions").document(doc_id) if db else None
        
        # 2. Check cache first
        if doc_ref:
            doc_snap = doc_ref.get()
            if doc_snap.exists:
                print(f"[Cache HIT] Found cached result for {doc_id}")
                cached_data = doc_snap.to_dict()
                result = cached_data.get("result")
                return {"status": "success", "data": result, "cached": True}
        
        print(f"[Cache MISS] Querying agent for {doc_id}...")
        # 3. Call the core computation function in agent.py
        result = run_compass_engine(req.target_job, req.mode)
        
        # 4. Save to cache asynchronously
        # Only cache structured successful responses, prevent caching fallback raw_text or errors
        is_valid_result = isinstance(result, dict) and "raw_text" not in result and result.get("status") != "error"
        if doc_ref and result and is_valid_result:
            doc_ref.set({
                "job": req.target_job,
                "mode": req.mode,
                "result": result,
                "timestamp": firestore.SERVER_TIMESTAMP
            })
            print(f"[Cache SAVE] Saved new deduction for {doc_id}")
            
        return {"status": "success", "data": result, "cached": False}
    except Exception as e:
        print(f"[Error] Deduction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files from the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the cyber-dark web UI at the root path
@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

# Health check interface
@app.get("/health")
def health_check():
    return {"status": "Compass API is running and ready for deduction!"}

if __name__ == "__main__":
    # Start using Uvicorn
    port = int(os.environ.get("PORT", 8081))
    uvicorn.run(app, host="0.0.0.0", port=port)