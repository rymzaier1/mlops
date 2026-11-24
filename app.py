
# ===== 1. Importer les bibliothèques =====
import os
from typing import Literal

import mlflow
import mlflow.sklearn
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel


# ===== 2. Créer l'application =====
app = FastAPI(title="API Churn")


# ===== 3. Lire la configuration dans les variables d'environnement =====
# Valeur par défaut : Registry MLflow local
TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "sqlite:///mlflow.db"
)

# Valeur par défaut : modèle champion du Registry
MODEL_URI = os.getenv(
    "MODEL_URI",
    "models:/churn-model@champion"
)


# ===== 4. Charger le modèle champion UNE SEULE FOIS =====
# Le modèle peut venir du Registry MLflow ou d'un dossier local.
mlflow.set_tracking_uri(TRACKING_URI)

modele = mlflow.sklearn.load_model(MODEL_URI)

print(f"Modèle chargé depuis : {MODEL_URI}")


# ===== 5. Décrire les données attendues =====
class Client(BaseModel):
    age: int
    salaire: float
    abonnement: Literal["Basique", "Standard", "Premium"]
    anciennete: float
    consommation: float


# ===== 6. Route /health : vérifier que l'API est en vie =====
@app.get("/health")
def verifier_etat():
    return {"status": "ok"}


# ===== 7. Route /predict : prédire le départ du client =====
@app.post("/predict")
def predire_depart(client: Client):

    # a) Convertir les informations reçues en DataFrame
    donnees = pd.DataFrame([client.model_dump()])

    # b) Encoder l'abonnement en colonnes binaires
    donnees = pd.get_dummies(donnees)

    # c) Adapter les colonnes à celles attendues par le modèle
    donnees = donnees.reindex(
        columns=modele.feature_names_in_,
        fill_value=0
    )

    # d) Effectuer la prédiction
    prediction = int(modele.predict(donnees)[0])

    # Retourner le résultat sous forme de JSON
    return {
        "churn": prediction,
        "message": (
            "Le client va partir"
            if prediction == 1
            else "Le client reste"
        )
    }
