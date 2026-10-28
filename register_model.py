
# ===== 1. Importation des modules nécessaires =====
import mlflow
from mlflow import MlflowClient

# ===== 2. Configuration de la base de données MLflow =====
# Utiliser la base de données contenant les expériences précédentes
mlflow.set_tracking_uri("sqlite:///mlflow.db")

# ===== 3. Recherche du meilleur modèle =====
# Récupérer les runs de l'expérience et les classer selon le score F1
runs = mlflow.search_runs(
    experiment_names=["churn-prediction"],
    order_by=["metrics.f1 DESC"]
)

# Sélectionner le run ayant le meilleur score F1
best_run = runs.iloc[0]
run_id = best_run["run_id"]

print(
    "Run sélectionné :",
    best_run["tags.mlflow.runName"],
    "| ID :",
    run_id[:8],
    "..."
)

# ===== 4. Ajout du modèle au Model Registry =====
# Enregistrer le modèle sélectionné sous le nom churn-model
model_uri = f"runs:/{run_id}/model"
registered_model = mlflow.register_model(
    model_uri=model_uri,
    name="churn-model"
)

print(
    "Modèle enregistré : churn-model | Version :",
    registered_model.version
)

# ===== 5. Attribution de l'alias champion =====
# Créer un client pour gérer les modèles enregistrés
client = MlflowClient()

# Désigner cette version comme modèle principal
client.set_registered_model_alias(
    name="churn-model",
    alias="champion",
    version=registered_model.version
)

print(
    "Alias 'champion' associé à la version",
    registered_model.version
)
