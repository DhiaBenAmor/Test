from models import db, Product, Client, Sale
from faker import Faker
import random
from datetime import datetime
from app import app

fake = Faker()

def generate_fake_data():
    with app.app_context():
        # Produits
        for _ in range(50):
            product = Product(
                name=fake.word(),
                category=random.choice(['Electronics', 'Clothing', 'Books']),
                price=round(random.uniform(10.0, 500.0), 2)
            )
            db.session.add(product)
        
        # Clients
        for _ in range(200):
            client = Client(
                name=fake.name(),
                email=fake.email()
            )
            db.session.add(client)
        
        # Ventes
        for _ in range(500):
            sale = Sale(
                product_id=random.randint(1, 50),
                client_id=random.randint(1, 200),
                sale_date=fake.date_time_this_year(),
                quantity=random.randint(1, 5),
                amount=round(random.uniform(10.0, 500.0), 2)
            )
            db.session.add(sale)

        db.session.commit()

if __name__ == '__main__':
    generate_fake_data()
