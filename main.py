from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysecretkey')

db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    category = db.relationship('Category', backref=db.backref('items', lazy=True))

# Роутинг для получения всех элементов
@app.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    result = []
    for item in items:
        item_data = {}
        item_data['id'] = item.id
        item_data['name'] = item.name
        item_data['description'] = item.description
        item_data['price'] = item.price
        item_data['category_id'] = item.category_id
        result.append(item_data)
    return jsonify(result)

# Роутинг для создания нового элемента
@app.route('/api/create_item', methods=['POST'])
def add_item():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    category_id = request.json['category_id']
    item = Item(name=name, description=description, price=price, category_id=category_id)
    db.session.add(item)
    db.session.commit()
    item_data = {}
    item_data['id'] = item.id
    item_data['name'] = item.name
    item_data['description'] = item.description
    item_data['price'] = item.price
    item_data['category_id'] = item.category_id
    return jsonify(item_data)

# Роутинг для получения элемента по id
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    item_data = {}
    item_data['id'] = item.id
    item_data['name'] = item.name
    item_data['description'] = item.description
    item_data['price'] = item.price
    item_data['category_id'] = item.category_id
    return jsonify(item_data)

# Роутинг для обновления элемента
@app.route('/api/update/<int:item_id>', methods=['GET', 'POST','PUT'])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        item.name = request.json['name']
        item.description = request.json['description']
        item.price = request.json['price']
        item.category_id = request.json['category_id']
        db.session.commit()
    else:
        item_data = {}
        item_data['id'] = item.id
        item_data['name'] = item.name
        item_data['description'] = item.description
        item_data['price'] = item.price
        item_data['category_id'] = item.category_id
        return jsonify(item_data)

# Роутинг для удаления элемента
@app.route('/api/delete/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return '', 204


app.run()
