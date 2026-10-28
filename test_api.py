
# ===== 1. Importation de la bibliothèque HTTP =====
import requests

# Adresse locale du serveur FastAPI
url = "http://localhost:8000"

# ===== 2. Vérification du fonctionnement de l'API =====
reponse = requests.get(url + "/health")
print("État de l'API :", reponse.json())

# ===== 3. Test de prédiction pour un premier client =====
# Client avec une ancienneté et une consommation faibles
client1 = {
    "age": 35,
    "salaire": 2500,
    "abonnement": "Standard",
    "anciennete": 1,
    "consommation": 10
}

reponse = requests.post(url + "/predict", json=client1)
print("Résultat du client 1 :", reponse.status_code, reponse.json())

# ===== 4. Test de prédiction pour un deuxième client =====
# Client avec une ancienneté et une consommation élevées
client2 = {
    "age": 50,
    "salaire": 4000,
    "abonnement": "Premium",
    "anciennete": 10,
    "consommation": 80
}

reponse = requests.post(url + "/predict", json=client2)
print("Résultat du client 2 :", reponse.status_code, reponse.json())

# ===== 5. Vérification de la validation des données =====
# Envoyer volontairement un âge invalide sous forme de texte
client_invalide = dict(client1, age="abc")

reponse = requests.post(url + "/predict", json=client_invalide)

print("Code HTTP pour les données invalides :", reponse.status_code)
print("Détail de l'erreur :", reponse.json()["detail"][0]["msg"])
