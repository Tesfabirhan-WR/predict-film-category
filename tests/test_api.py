import csv
import os
from pathlib import Path

from check_quality import check, load_config, load_metrics

ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = Path("/home/projects/predict-film-category/model")
FAKE_METRICS = ROOT / "tests" / "fake_model" / "metrics.json"

VALID_TEXT = "A group of friends is hunted by a masked killer in an abandoned cabin deep in the woods."
LABELS = {"1": "horror", "0": "comedy"}


# --- The API responds -------------------------------------------------------
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_version"]
    assert "commit" in body


# --- A valid case works -----------------------------------------------------
def test_predict_valid_text(client):
    response = client.post("/predict", json={"text": VALID_TEXT})
    assert response.status_code == 200
    body = response.json()
    assert body["category"] in {"horror", "comedy"}
    assert 0.5 <= body["probability"] <= 1.0
    assert body["version"]


# --- Invalid cases are refused with a clear message -------------------------
def test_predict_empty_text_is_refused(client):
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422
    body = response.json()
    assert body["error"]
    assert body["details"]


def test_predict_very_short_text_is_refused(client):
    response = client.post("/predict", json={"text": "Scary movie"})
    assert response.status_code == 422
    assert "text" in " ".join(response.json()["details"])


def test_predict_missing_field_is_refused(client):
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_predict_text_without_usable_words_is_refused(client):
    response = client.post("/predict", json={"text": "12345 67890 !!!! ???? 00000"})
    assert response.status_code == 422
    assert response.json()["detail"]


# --- The model reaches a minimum score --------------------------------------
def test_metrics_meet_the_quality_thresholds():
    assert check(load_metrics(MODEL_DIR / "metrics.json"), load_config()) == []


def test_reference_sample_through_the_api(client):
    """Smoke test of the whole chain (cleaning + TF-IDF + network) on the saved reference sample.

    The sample comes from the training set, so this checks that the deployed files work,
    not how well the model generalises (that is what the test F1 in metrics.json is for).
    """
    with open(MODEL_DIR / "reference_sample.csv", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert rows, "reference_sample.csv is empty"

    correct = 0
    for row in rows:
        response = client.post("/predict", json={"text": row["resume"]})
        assert response.status_code == 200, response.text
        correct += response.json()["category"] == LABELS[row["cible"]]

    accuracy = correct / len(rows)
    assert accuracy >= load_config()["min_reference_accuracy"], f"accuracy {accuracy:.2f}"


# --- The quality gate itself works ------------------------------------------
def test_quality_gate_rejects_a_fake_bad_model():
    problems = check(load_metrics(FAKE_METRICS), load_config())
    assert problems, "the fake model (F1 0.31) should have been refused"
