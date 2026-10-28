
# ===== 1. Charger les bibliothèques nécessaires =====
import mlflow
import mlflow.sklearn
import pandas as pd

# ===== 2. Configurer l'accès à la base MLflow =====
mlflow.set_tracking_uri("sqlite:///mlflow.db")

# ===== 3. Récupérer le modèle associé à l'alias champion =====
modele = mlflow.sklearn.load_model("models:/churn-model@champion")

print("Modèle chargé :", type(modele).__name__)
print("Liste des variables requises :", list(modele.feature_names_in_))

# ===== 4. Préparer les informations d'un nouveau client =====
# Les catégories d'abonnement sont déjà encodées en valeurs booléennes
donnees_client = pd.DataFrame([{
    "age": 35,
    "salaire": 2500,
    "anciennete": 1,
    "consommation": 10,
    "abonnement_Premium": False,
    "abonnement_Standard": True
}])

# ===== 5. Adapter les données au format attendu =====
# Conserver les variables nécessaires dans le même ordre que lors de l'entraînement
donnees_client = donnees_client[list(modele.feature_names_in_)]

# ===== 6. Déterminer si le client risque de partir =====
prediction = modele.predict(donnees_client)[0]

print(
    "Le client va-t-il partir ? ->",
    "OUI" if prediction == 1 else "NON"
)
