
import mlflow  # Réutiliser MLflow pour lire les résultats

# search_runs renvoie tous les runs de l'expérience sous forme de tableau pandas.
# order_by trie les lignes : "metrics.f1 DESC" = F1 décroissant
# (le meilleur résultat en premier)
runs = mlflow.search_runs(
    experiment_names=["churn-prediction"],
    order_by=["metrics.f1 DESC"]
)

# Colonnes à afficher : nom du run, deux paramètres et deux métriques
colonnes = [
    "tags.mlflow.runName",
    "params.n_estimators",
    "params.max_depth",
    "metrics.accuracy",
    "metrics.f1"
]

# Afficher le tableau sans numéros de ligne
print(runs[colonnes].to_string(index=False))

# La première ligne du tableau trié correspond au meilleur run
meilleur = runs.iloc[0]

print()

# [:8] : afficher uniquement les 8 premiers caractères de l'identifiant
print(
    "Meilleur run :",
    meilleur["tags.mlflow.runName"],
    "| id :",
    meilleur["run_id"][:8],
    "..."
)
