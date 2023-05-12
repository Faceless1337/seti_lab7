from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/index.html')
def index():
    # делаем запрос на REST сервер и получаем список элементов
    response = requests.get('http://localhost:5000/api/items')
    items = response.json()

    # генерируем HTML
    return render_template('index.html', items=items)



@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # делаем запрос на REST сервер и получаем элемент по id
    response = requests.get(f'http://localhost:5000/api/update/{id}')
    item = response.json()

    if request.method == 'POST':
        print(request.form['category_id'])
        # отправляем запрос на REST сервер для обновления элемента
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'price': request.form['price'],
            'category_id': request.form['category_id']
        }
        requests.post(f'http://localhost:5000/api/update/{id}', json=data)
        return redirect(url_for('index'))

    # генерируем HTML
    return render_template('edit.html', item=item)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    # отправляем запрос на REST сервер для удаления элемента
    requests.delete(f'http://localhost:5000/api/delete/{id}')
    return redirect(url_for('index'))

@app.route('/add.html', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # отправляем запрос на REST сервер для добавления нового элемента
        data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'price': request.form['price'],
        'category_id': request.form['category_id']
        }
        requests.post('http://localhost:5000/api/create_item', json=data)
        return redirect(url_for('index'))
    else:
        return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True, port=5050)