from kmeans import train_kmeans_model, visualize_clusters , analyze_clusters
from models import db, Product
from app import app  # Importez l'application Flask

def main():
    with app.app_context():  # Créer un contexte d'application
        # Obtenir les produits pour former le modèle
        products = db.session.query(Product.id, Product.name, Product.category, Product.price).all()

        # Former le modèle K-means
        product_data , kmeans = train_kmeans_model(products)

        # Visualiser les clusters
        visualize_clusters(product_data,kmeans)

        cluster_summary = analyze_clusters(product_data,kmeans)
        print(cluster_summary)

if __name__ == '__main__':
    main()
