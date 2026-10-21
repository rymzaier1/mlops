
import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


# ===== 1. Charger et préparer les données =====
df = pd.read_csv("churn_data.csv")

X = pd.get_dummies(
    df[["age", "salaire", "abonnement", "anciennete", "consommation"]],
    drop_first=True
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    df["churn"],
    test_size=0.2,
    random_state=42
)


# ===== 2. Configurer l'expérience MLflow =====
mlflow.set_experiment("churn-prediction")


# Activer l'enregistrement automatique pour scikit-learn :
# MLflow enregistre automatiquement les paramètres du modèle,
# les métriques et le modèle lui-même.
mlflow.sklearn.autolog(
    serialization_format="cloudpickle"
)


# ===== 3. Entraîner le modèle et enregistrer l'essai =====
with mlflow.start_run(run_name="essai-auto"):

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=4,
        random_state=42
    )

    # L'enregistrement automatique se déclenche au fit()
    model.fit(X_train, y_train)

    # score() calcule l'accuracy sur les données de test
    print("Score test :", model.score(X_test, y_test))
