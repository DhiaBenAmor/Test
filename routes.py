from flask import Blueprint, jsonify
from models import db, Product, Sale, Client
from sqlalchemy import func

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
