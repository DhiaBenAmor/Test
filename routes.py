from flask import Blueprint, jsonify
from models import db, Product, Sale, Client
from sqlalchemy import func
from kmeans import train_kmeans_model 
import pandas as pd

api = Blueprint('api', __name__)

# Endpoint pour le nombre total de ventes et le montant total des ventes
@api.route('/stats/sales/total', methods=['GET'])
def total_sales():
    total_count = Sale.query.count()
    total_amount = db.session.query(func.sum(Sale.amount)).scalar() or 0
    return jsonify({'total_sales': total_count, 'total_amount': total_amount})

# Endpoint pour le produit ayant généré le plus de revenus
@api.route('/stats/sales/best-product', methods=['GET'])
def best_product():
    best_product = db.session.query(
        Product.name,
        func.sum(Sale.amount).label('total_revenue')
    ).join(Sale).group_by(Product.id).order_by(func.sum(Sale.amount).desc()).first()
    return jsonify({'best_product': best_product.name, 'revenue': best_product.total_revenue})

# Endpoint pour le total des ventes par catégorie de produits
@api.route('/stats/sales/by-category', methods=['GET'])
def sales_by_category():
    result = db.session.query(
        Product.category,
        func.sum(Sale.amount).label('total_revenue')
    ).join(Sale).group_by(Product.category).all()
    return jsonify([{ 'category': row.category, 'total_revenue': row.total_revenue } for row in result])

# Endpoint pour le nombre de ventes et montant total des ventes par mois
@api.route('/stats/sales/by-month', methods=['GET'])
def sales_by_month():
    result = db.session.query(
        func.date_format(Sale.sale_date, '%Y-%m').label('month'),
        func.count(Sale.id).label('sales_count'),
        func.sum(Sale.amount).label('total_amount')
    ).group_by('month').all()
    return jsonify([{ 'month': row.month, 'sales_count': row.sales_count, 'total_amount': row.total_amount } for row in result])


# Endpoint pour recommander des produits à un client
@api.route('/recommandations/<int:client_id>', methods=['GET'])
def recommend_products(client_id):
    # Obtenir la catégorie la plus achetée par le client
    favorite_category = db.session.query(
        Product.category,
        func.count(Sale.id).label('purchase_count')
    ).join(Sale).filter(Sale.client_id == client_id).group_by(Product.category).order_by(func.count(Sale.id).desc()).first()

    # Si le client a une catégorie préférée, recommander des produits de cette catégorie
    if favorite_category:
        recommended_products = Product.query.filter_by(category=favorite_category.category).limit(3).all()
    else:
        # Sinon, recommander les produits les plus populaires globalement
        recommended_products = db.session.query(Product).limit(3).all()

    return jsonify([{'product_name': product.name, 'category': product.category, 'price': product.price} for product in recommended_products])




def recommend_products_kmeans(client_id):
    # Obtenir la moyenne des dépenses du client
    average_spent = db.session.query(func.avg(Sale.amount)).filter(Sale.client_id == client_id).scalar() or 0

    # Récupérer tous les produits pour former le modèle K-means
    products = db.session.query(Product.id, Product.name,Product.category, Product.price).all()
    
    # Convertir en DataFrame pour le traitement
    product_df = pd.DataFrame(products, columns=['id', 'name','category', 'price'])

    # Former le modèle K-means et obtenir les données de clustering
    product_data, kmeans_model = train_kmeans_model(product_df)

    # Ajouter une colonne de cluster au DataFrame des produits
    product_data['cluster'] = kmeans_model.predict(product_data[['price']])  

    # Déterminer le cluster correspondant à la moyenne des dépenses du client
    if average_spent < 180:  #  faible dépense
        cluster_to_recommend = 2  
    elif average_spent >= 180 and average_spent < 330:  # dépense moyenne
        cluster_to_recommend = 0  
    else:
        cluster_to_recommend = 1  

    # Filtrer les produits dans le cluster recommandé
    recommended_products = product_data[product_data['cluster'] == cluster_to_recommend]

    # Sélectionner un produit à recommander (par exemple, le plus acheté dans le cluster)
    if not recommended_products.empty:
        recommended_product = recommended_products.iloc[0]  # Prendre le premier produit dans le cluster
    else:
        return jsonify({'message': 'Aucun produit disponible dans ce cluster.'})

    return jsonify({
        'Avg_client_spent': average_spent,
        'product_name': recommended_product['name'],
        'price': recommended_product['price'],
        'category': recommended_product['category']
    })
@api.route('/recommandationskmeans/<int:client_id>', methods=['GET'])
def get_recommendations(client_id):
    return recommend_products_kmeans(client_id)