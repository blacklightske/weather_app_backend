from flask import Flask, jsonify, request
import sqlite3
app= Flask(__name__)
# products = [
#         {
#             "id": 1, "name": "keyboard", "price": 49.99

#         },
#         {
#             "id": 2, "name": "Mouse", "price": 29.99

#         }
#     ]

def get_db_connection():
    conn= sqlite3.connect('products.db')
    #test without the below line 
    print("we are showing data ")
     # converts the tuples into objects easily readable with python
    return conn

@app.route("/init", methods=["GET"])
def init_db():
    conn = get_db_connection()
    conn.execute("""
                CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
                )
                """)
    conn.commit()
    conn.close()
    return jsonify({"message": "Database initialized"})


@app.route("/")
def home():
    return jsonify({"message":"hello from our first flask server"})

@app.route("/products", methods=["GET"])
def get_products():
   conn = get_db_connection()
   rows = conn.execute("SELECT * FROM products").fetchall()
   conn.close()
   return jsonify([dict(row)for row in rows])# convert rows into  a python dictionary list 

@app.route("/products", methods=["POST"])
def add_products():
    data= request.get_json()#its converting from user input to json so that it may be manipulated or saved to server ..its from client to server 
    name= data.get("name")
    price = data.get("price")
    conn = get_db_connection() #creates a cursor tied to that DB connection
    cursor = conn.cursor() # cursor is the object that sends SQL to the database and gives you back results/details.
    cursor =cursor.execute("INSERT INTO products (name, price) VALUES (?,?)",(name,price))# the ?? prevent sql injection 
    conn.commit() #saves changes to db
    new_id = cursor.lastrowid
    conn.close()# x// many open coonctions crash the server
   
    new_product = {
        "id": new_id,
        "name":name,
        "price":price

    }
    return jsonify({"message":"product added safetly","product": new_product}), 201
    
#GET-2,PUT/PATCH,  DELETE, 
if __name__== "__main__":
    #initialize db whenever app is run 
    with app.app_context():
     init_db()
    app.run(debug=True)#without debug set to true the app will not auti reload server when code changes and it will show less error tracebacks