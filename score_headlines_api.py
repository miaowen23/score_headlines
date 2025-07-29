from fastapi import FastAPI, Request
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import joblib
import logging
import uvicorn

# ---------- Logging setup ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# ---------- FastAPI App ----------
app = FastAPI()

# ---------- Load model once ----------
try:
    logging.info("Loading transformer and classifier...")
    transformer = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
    classifier = joblib.load("svm.joblib")
    logging.info("Models loaded successfully.")
except Exception as e:
    logging.critical(f"Failed to load models: {e}")
    raise

# ---------- Pydantic request schema ----------
class HeadlineRequest(BaseModel):
    headlines: list[str]

# ---------- /status endpoint ----------
@app.get("/status")
def status():
    logging.info("Status check received.")
    return {"status": "OK"}

# ---------- /score_headlines endpoint ----------
@app.post("/score_headlines")
def score_headlines(request: HeadlineRequest):
    try:
        logging.info(f"Received {len(request.headlines)} headlines for scoring.")
        vectors = transformer.encode(request.headlines)
        labels = classifier.predict(vectors).tolist()
        return {"labels": labels}
    except Exception as e:
        logging.error(f"Error scoring headlines: {e}")
        return {"error": str(e)}
