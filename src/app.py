"""API de classification de films (horreur / comédie).

Routes :
    GET  /health   -> statut, version du modèle, identifiant du commit
    POST /predict  -> classe, probabilité, version
"""
import json
import os
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import spacy
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
import keras

MODEL_DIR = Path(os.getenv("MODEL_DIR", Path(__file__).resolve().parent.parent / "model"))
COMMIT = os.getenv("GIT_COMMIT", "unknown")  # injecté à la construction de l'image
LABELS = {1: "horror", 0: "comedy"}  # même convention que le notebook
MIN_CHARS = 20
MAX_CHARS = 5000


def clean_doc(doc):
    """Même nettoyage que dans le notebook : lemmes en minuscules, sans mots vides."""
    return " ".join(t.lemma_.lower() for t in doc if t.is_alpha and not t.is_stop)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Charge le modèle une seule fois, au démarrage."""
    app.state.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    app.state.vectorizer = joblib.load(MODEL_DIR / "tfidf.joblib")
    app.state.model = keras.models.load_model(MODEL_DIR / "model.keras")
    with open(MODEL_DIR / "metrics.json", encoding="utf-8") as f:
        app.state.metrics = json.load(f)
    yield


app = FastAPI(title="Film Category API", lifespan=lifespan)


class PredictRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    text: str = Field(
        ...,
        min_length=MIN_CHARS,
        max_length=MAX_CHARS,
        description=f"Résumé du film en anglais ({MIN_CHARS} à {MAX_CHARS} caractères).",
    )


class PredictResponse(BaseModel):
    category: str
    probability: float
    version: str


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    details = [f"{'.'.join(str(p) for p in e['loc'][1:]) or 'body'}: {e['msg']}" for e in exc.errors()]
    return JSONResponse(status_code=422, content={"error": "Requête invalide", "details": details})


@app.get("/health")
def health():
    return {"status": "ok", "model_version": app.state.metrics["model_version"], "commit": COMMIT}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    cleaned = clean_doc(app.state.nlp(request.text))
    if not cleaned:
        raise HTTPException(
            status_code=422,
            detail="Le texte ne contient aucun mot exploitable : envoyez un résumé de film en anglais.",
        )

    features = app.state.vectorizer.transform([cleaned]).toarray().astype("float32")
    p_horror = float(app.state.model.predict(features, verbose=0).ravel()[0])
    label = 1 if p_horror > 0.5 else 0

    return PredictResponse(
        category=LABELS[label],
        probability=round(p_horror if label == 1 else 1 - p_horror, 4),
        version=app.state.metrics["model_version"],
    )
