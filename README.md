# API de Vente

Cette API permet d'analyser les données de ventes d'une société de vente en ligne. Elle fournit des statistiques sur les ventes passées et inclut un système de recommandations de produits.


## Fonctionnalités
- Statistiques de ventes totales
- Produit générant le plus de revenus
- Ventes par catégorie
- Ventes par mois
- Recommandations de produits basées sur les achats passés d'un client
- Recommandations de produits basées sur les achats passés d'un client avec le modèle K-means

## Installation
1. Clonez le repository :
   ```bash
   git clone https://github.com/DhiaBenAmor/Test.git
   ```

## Créez un environnement virtuel :

```bash
python -m venv venv
source venv/bin/activate  # Pour Linux/Mac
venv\Scripts\activate  # Pour Windows
```

Installez les dépendances :
```
pip install -r requirements.txt
```
## Configuration de la base de données

1) Assurez-vous que MySQL est installé et en cours d'exécution.

2) Créez une base de données nommée test :
```SQL:
CREATE DATABASE test;
```

Modifiez le fichier config.py si nécessaire pour correspondre à votre configuration de base de données.


## Endpoints de l'API
- GET /stats/sales/total : Retourne le nombre total de ventes et le montant total des ventes.
- GET /stats/sales/best-product : Retourne le produit ayant généré le plus de revenus
- GET /stats/sales/by-category : Retourne le total des ventes et le montant des ventes par catégorie de produits.
- GET /stats/sales/by-month : Retourne le nombre de ventes et le montant total des ventes pour chaque mois de l'année.
- GET /recommandations/{client_id} : Retourne une liste de 3 produits recommandés pour un client donné.
- GET //recommandationskmeans/<int:client_id> : Retourne un produit recommandé pour un client donné.

## Tester l'API
Vous pouvez tester l'API de plusieurs manières :

Postman : Utilisez Postman pour envoyer des requêtes HTTP aux différents endpoints.

Swagger UI : Accédez à la documentation Swagger de l'API en allant sur l'URL suivante : http://localhost:5000/swagger. Vous pouvez interagir avec l'API directement via cette interface.
## Visualisation des Clusters

Le fichier `visualize_clusters.py` vous permet de visualiser les clusters formés par le modèle K-means sur les produits en se basant sur le prix

### Exécution de `visualize_clusters.py`

1. **Assurez-vous d'avoir installé toutes les dépendances**. Si ce n'est pas déjà fait, utilisez la commande suivante pour installer les bibliothèques nécessaires :
   ```bash
   pip install -r requirements.txt


Exécutez le script : Vous pouvez exécuter le fichier visualize_clusters.py avec la commande suivante :

```bash
python visualize_clusters.py
```


