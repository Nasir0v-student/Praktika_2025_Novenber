from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Модель Product (книги)
class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    photo = db.Column(db.String(200))

    def __repr__(self):
        return f'<Product {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'photo': self.photo
        }

# HTML страницы
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def products_page():
    """Страница с товарами"""
    return render_template("products.html")

# API endpoints для работы с товарами
@app.route("/api/product/all")
def get_products_api():
    try:
        products_list = Product.query.all()
        result = [product.to_dict() for product in products_list]
        return jsonify(result)
    except Exception as e:
        return Response(jsonify({"status": "500", "message": f"Database error: {str(e)}"}), status=500)

@app.route("/api/product", methods=["POST"])
def add_product_api():
    if request.method == "POST":
        try:
            data = request.get_json() if request.is_json else request.form
            
            new_product = Product(
                name=data.get("name"),
                description=data.get("description"),
                price=float(data.get("price")),
                photo=data.get("photo", data.get("image", ""))
            )
            
            db.session.add(new_product)
            db.session.commit()
            
            return jsonify(new_product.to_dict())
        except Exception as e:
            return jsonify({"message": f"Error: {str(e)}"}), 500

@app.route("/api/product/<int:id>", methods=["GET", "DELETE", "PUT"])
def product_api(id):
    try:
        product = Product.query.get(id)
        
        if request.method == "GET":
            if product:
                return jsonify(product.to_dict())
            else:
                return jsonify({"message": "Product not found"}), 404
        
        if request.method == "DELETE":
            if product:
                db.session.delete(product)
                db.session.commit()
                return jsonify({"message": "Success", "id": id})
            else:
                return jsonify({"message": "Product not found"}), 404
        
        if request.method == "PUT":
            if product:
                data = request.get_json() if request.is_json else request.form
                
                product.name = data.get("name", product.name)
                product.description = data.get("description", product.description)
                product.price = float(data.get("price", product.price))
                product.photo = data.get("photo", data.get("image", product.photo))
                
                db.session.commit()
                return jsonify(product.to_dict())
            else:
                return jsonify({"message": "Product not found"}), 404
                
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# Админка для управления товарами
@app.route("/admin/products", methods=['GET', 'POST'])
def admin_products():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        photo = request.form.get('photo', '')

        new_product = Product(name=name, description=description, price=float(price), photo=photo)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('admin_products'))

    products_list = Product.query.all()
    return render_template("admin_products.html", products=products_list)

@app.route("/admin/products/delete/<int:product_id>", methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('admin_products'))

def main():
    with app.app_context():
        db.create_all()

        # Добавим начальные записи для продуктов (книг)
        if not Product.query.first():
            product1 = Product(
                name="Война и мир", 
                description="Роман-эпопея Льва Толстого", 
                price=1500.0, 
                photo="https://via.placeholder.com/300x400/007bff/ffffff?text=Война+и+мир"
            )
            product2 = Product(
                name="Преступление и наказание", 
                description="Роман Фёдора Достоевского", 
                price=1200.0, 
                photo="https://via.placeholder.com/300x400/28a745/ffffff?text=Преступление+и+наказание"
            )
            product3 = Product(
                name="Мастер и Маргарита", 
                description="Роман Михаила Булгакова", 
                price=1300.0, 
                photo="https://via.placeholder.com/300x400/dc3545/ffffff?text=Мастер+и+Маргарита"
            )
            product4 = Product(
                name="Евгений Онегин", 
                description="Роман в стихах Александра Пушкина", 
                price=1100.0, 
                photo="https://via.placeholder.com/300x400/ffc107/000000?text=Евгений+Онегин"
            )
            db.session.add_all([product1, product2, product3, product4])
            db.session.commit()

    app.run("localhost", port=8000, debug=True)

if __name__ == "__main__":
    main()