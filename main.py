# Filename: main.py
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent import run_compass_engine

# Initialize a clean FastAPI engine
app = FastAPI(title="Compass Oracle API")

# Define strict input parameter validation
class CompassRequest(BaseModel):
    target_job: str
    mode: str = "mixed"  # Defaults to mixed mode

# Core compass deduction interface (handles POST requests)
@app.post("/compass")
def generate_compass(req: CompassRequest):
    try:
        print(f"[Compass] Received deduction request: job={req.target_job}, mode={req.mode}")
        # Call the core computation function in agent.py
        result = run_compass_engine(req.target_job, req.mode)
        return {"status": "success", "data": result}
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