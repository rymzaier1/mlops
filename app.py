
# ===== 1. Importation des modules =====
from typing import Literal
import mlflow
import mlflow.sklearn
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# ===== 2. Initialisation de l'API =====
app = FastAPI(title="API Churn")

# ===== 3. Récupération du modèle champion =====
# Charger le modèle une seule fois lors du lancement de l'application
mlflow.set_tracking_uri("sqlite:///mlflow.db")
modele = mlflow.sklearn.load_model("models:/churn-model@champion")

# ===== 4. Définition du format des informations client =====
class Client(BaseModel):
    age: int
    salaire: float
    abonnement: Literal["Basique", "Standard", "Premium"]
    anciennete: float
    consommation: float

# ===== 5. Endpoint de contrôle de disponibilité =====
@app.get("/health")
def verifier_etat():
    return {"status": "ok"}

# ===== 6. Endpoint de prédiction du départ client =====
@app.post("/predict")
def predire_depart(client: Client):

    # Convertir les informations reçues en DataFrame
    donnees = pd.DataFrame([client.model_dump()])

    # Encoder la catégorie d'abonnement en variables binaires
    donnees = pd.get_dummies(donnees)

    # Adapter les colonnes à celles attendues par le modèle
    # Ajouter les colonnes manquantes avec la valeur 0
    donnees = donnees.reindex(
        columns=modele.feature_names_in_,
        fill_value=0
    )

    # Effectuer la classification du client
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
