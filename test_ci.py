
import os

os.environ["MODEL_URI"] = "model"

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

CLIENT = {
    "age": 35,
    "salaire": 2500,
    "abonnement": "Standard",
    "anciennete": 1,
    "consommation": 10
}


def test_health():
    reponse = client.get("/health")
    assert reponse.status_code == 200
    assert reponse.json() == {"status": "ok"}


def test_client_a_risque_part():
    reponse = client.post("/predict", json=CLIENT)
    assert reponse.status_code == 200
    assert reponse.json()["churn"] == 1


def test_client_fidele_reste():
    fidele = dict(
        CLIENT,
        age=50,
        salaire=4000,
        abonnement="Premium",
        anciennete=10,
        consommation=80
    )

    reponse = client.post("/predict", json=fidele)
    assert reponse.status_code == 200
    assert reponse.json()["churn"] == 0


def test_donnee_invalide_refusee():
    mauvais = dict(CLIENT, age="abc")
    reponse = client.post("/predict", json=mauvais)
    assert reponse.status_code == 422
