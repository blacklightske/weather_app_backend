from flask import Flask
from routes.product_routes import product_bp
from config import Config
from db.database import db
from models.product import Product #ensure flask sees  model before create_all

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app) # connects ORM to flask app  

app.register_blueprint(product_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # replaces init_db() creates tables automatically based on models
    app.run(debug=True)