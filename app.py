from flask import Flask
from models import db
from routes import api
from config import Config
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config.from_object(Config)


# Initialisation de la base de données
db.init_app(app)

with app.app_context():
    db.create_all()

# Swagger configuration
SWAGGER_URL = '/swagger'  # URL pour accéder à la documentation
API_URL = '/static/swagger.yaml'  # Chemin vers le fichier YAML
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  
    API_URL, 
    config={  
        'app_name': "API de ventes"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Enregistrement des routes de l'API
app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True)
