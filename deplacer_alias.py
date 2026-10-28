
# ===== 1. Importation des outils MLflow =====
import mlflow
from mlflow import MlflowClient

# Connexion à la base de données des expériences
mlflow.set_tracking_uri("sqlite:///mlflow.db")
client = MlflowClient()

# ===== 2. Recherche du run essai-2 =====
# Identifier l'exécution correspondant à l'expérience essai-2
resultats = mlflow.search_runs(
    experiment_names=["churn-prediction"],
    filter_string="tags.mlflow.runName = 'essai-2'"
)

id_run = resultats.iloc[0]["run_id"]

# ===== 3. Enregistrement d'une nouvelle version du modèle =====
# Ajouter le modèle de ce run au catalogue churn-model
nouvelle_version = mlflow.register_model(
    f"runs:/{id_run}/model",
    "churn-model"
)

print("Version nouvellement créée :", nouvelle_version.version)

# ===== 4. Vérification de l'alias champion =====
# Identifier la version actuellement désignée comme champion
ancien_champion = client.get_model_version_by_alias(
    "churn-model",
    "champion"
)

print("Champion avant modification : version", ancien_champion.version)

# ===== 5. Modification temporaire de l'alias =====
# Faire pointer champion vers la nouvelle version
client.set_registered_model_alias(
    "churn-model",
    "champion",
    nouvelle_version.version
)

print(
    "Après modification : champion -> version",
    client.get_model_version_by_alias("churn-model", "champion").version
)

# ===== 6. Restauration de l'alias initial =====
# Réattribuer champion à la version qui était utilisée auparavant
client.set_registered_model_alias(
    "churn-model",
    "champion",
    ancien_champion.version
)

print(
    "Après restauration : champion -> version",
    client.get_model_version_by_alias("churn-model", "champion").version
)
