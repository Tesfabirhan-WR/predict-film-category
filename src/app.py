"""API de classification de films (horreur / comédie).

Routes :
    GET  /          -> page d'accueil avec le logo
    GET  /health    -> statut, version du modèle, identifiant du commit
    POST /predict   -> classe, probabilité, version
    GET  /docs      -> page de test (Swagger) avec le logo
"""
import json
import os
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import spacy
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field
import keras

MODEL_DIR = Path(os.getenv("MODEL_DIR", Path(__file__).resolve().parent.parent / "model"))
STATIC_DIR = Path(__file__).resolve().parent / "static"  # logo.png, favicon.ico
COMMIT = os.getenv("GIT_COMMIT", "unknown")  # injecté à la construction de l'image
LABELS = {1: "horror", 0: "comedy"}  # même convention que le notebook
MIN_CHARS = 20
MAX_CHARS = 5000

DESCRIPTION = (
    '<img src="/static/logo.png" alt="Film Category API logo" width="120">\n\n'
    "Predicts whether a film summary (in English) is a **horror** film or a **comedy**."
)


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


# docs_url=None : la page /docs est redéfinie plus bas pour afficher le favicon
app = FastAPI(title="Film Category API", description=DESCRIPTION, lifespan=lifespan, docs_url=None)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def custom_openapi():
    """Ajoute le logo à la page /redoc."""
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(title=app.title, version=app.version, description=app.description, routes=app.routes)
    schema["info"]["x-logo"] = {"url": "/static/logo.png"}
    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi


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


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home():
    return """<<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Film Category API</title>
  <link rel="icon" href="/favicon.ico">
  <style>
    body { font-family: system-ui, sans-serif; text-align: center; margin: 4rem 1rem; color: #1f2937; }
    .logo { width: 200px; height: 200px; border-radius: 16px; }
    .curves { width: 100%; max-width: 900px; height: auto; }
    a { color: #1d4ed8; margin: 0 .6rem; }
  </style>
</head>
<body>
  <img class="logo" src="/static/logo.png" alt="Film Category API logo">
  <h1>Film Category API</h1>
  <p>Send a film summary, get back <strong>horror</strong> or <strong>comedy</strong>.</p>
  <p><a href="/docs">Try it (Swagger)</a> <a href="/redoc">Documentation</a> <a href="/health">Health</a></p>

  <h2>Training curves</h2>
  <img class="curves" src="/static/training_curves.png" alt="Training curves: loss and accuracy of the final model">
</body>
</html>"""


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse(STATIC_DIR / "favicon.ico")


@app.get("/docs", include_in_schema=False)
def swagger_ui():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - docs",
        swagger_favicon_url="/static/favicon.ico",
    )


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
