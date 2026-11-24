
# ===== 1. Importer les bibliothèques =====
import mlflow
import mlflow.sklearn


# ===== 2. Se connecter au Registry MLflow du TP4 =====
mlflow.set_tracking_uri("sqlite:///mlflow.db")


# ===== 3. Charger le modèle champion =====
modele = mlflow.sklearn.load_model(
    "models:/churn-model@champion"
)


# ===== 4. Exporter le modèle dans un dossier ordinaire =====
# Le dossier model sera utilisé dans l'image Docker.
mlflow.sklearn.save_model(
    modele,
    "model",
    serialization_format="cloudpickle"
)


# ===== 5. Confirmer l'exportation =====
print("Champion exporté dans le dossier model/")
