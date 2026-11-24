
import shutil
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("churn_data.csv")

X = pd.get_dummies(
    df.drop(columns=["churn"]),
    columns=["abonnement"]
)

y = df["churn"]

modele = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

modele.fit(X, y)

shutil.rmtree("model", ignore_errors=True)

mlflow.sklearn.save_model(
    modele,
    "model",
    serialization_format="cloudpickle"
)

print("Modèle entraîné et écrit dans le dossier model/")
