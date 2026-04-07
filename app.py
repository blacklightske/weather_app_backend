from flask import Flask
from routes.product_routes import product_bp
from config import Config
from db.database import db
from models.product import Product
from flask_migrate import Migrate
from models.category import Category

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(product_bp)

if __name__ == "__main__":
    #with app.app_context():
       # db.create_all() #creates missing tables not modify existing ones 
    app.run(debug=True)