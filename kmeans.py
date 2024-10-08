import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder


def train_kmeans_model(products):
    # Convertir les produits en DataFrame
    product_data = pd.DataFrame(products, columns=['id', 'name', 'category', 'price'])

    # Les caractéristiques pour K-means (price)
    X = product_data[['price']]  

    # Créer et entraîner le modèle K-means
    kmeans_model = KMeans(n_clusters=3)
    product_data['cluster'] = kmeans_model.fit_predict(X)

    return product_data, kmeans_model  # Retourner les données et le modèle





def visualize_clusters(product_data, kmeans_model):
    # Visualisation des clusters avec Matplotlib et Seaborn
    plt.figure(figsize=(10, 6))
    
    # Visualiser les clusters en fonction du prix
    sns.scatterplot(x='price', y='cluster', hue='cluster', data=product_data, palette='Set1', s=100)

    # Ajouter les centres des clusters (pour la caractéristique 'price' seulement)
    centers = kmeans_model.cluster_centers_
    plt.scatter(centers[:, 0], [0] * len(centers), c='black', s=200, alpha=0.5)
    
    plt.title('Clusters de produits (basé sur le prix)')
    plt.xlabel('Price')
    plt.ylabel('Cluster')
    plt.show()


def analyze_clusters(product_data, kmeans_model):
    # Ajouter une colonne de cluster aux données des produits
    product_data['cluster'] = kmeans_model.labels_

    # Analyser les caractéristiques par cluster
    cluster_summary = product_data.groupby('cluster').agg({
        'price': ['mean', 'min', 'max', 'count'],  # Exemple avec le prix
        'name': lambda x: ', '.join(x)  # Lister les noms des produits
    }).reset_index()

    # Renommer les colonnes pour une meilleure lisibilité
    
    cluster_summary.columns = ['Cluster', 'Average Price', 'Min Price', 'Max Price', 'Product Count', 'Product List']
    
    return cluster_summary