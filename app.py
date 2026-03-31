from flask import Flask
from routes.product_routes import product_bp
from db.database import init_db

app = Flask(__name__)

app.register_blueprint(product_bp)

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)