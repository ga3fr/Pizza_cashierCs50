from datetime import datetime
from flask import Flask, render_template_string, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu.db'
db = SQLAlchemy(app)


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    date_added = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    time_added = db.Column(db.Time, nullable=False, default=datetime.utcnow().time)

db.create_all()
@app.route('/')
def index():
    items = MenuItem.query.all()
    return render_template('index.html', items=items, error=request.args.get('error'))
    return render_template_string('''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Menu</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; }
            .container { width: 80%; margin: auto; overflow: hidden; }
            header { background: #333; color: #fff; padding: 10px 0; text-align: center; }
            h1 { margin: 0; }
            .menu { background: #fff; padding: 20px; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
            ul { list-style: none; padding: 0; }
            li { padding: 10px; border-bottom: 1px solid #eee; }
            form { margin-top: 20px; }
            input[type="text"], input[type="number"] { padding: 10px; border: 1px solid #ccc; border-radius: 5px; width: calc(50% - 22px); margin-right: 10px; }
            button { padding: 10px 20px; border: none; background: #333; color: #fff; border-radius: 5px; cursor: pointer; }
            button:hover { background: #555; }
            .error { color: red; margin-top: 10px; }
        </style>
    </head>
    <body>
        <header>
            <h1>Menu</h1>
        </header>
        <div class="container">
            <div class="menu">
                <ul>
                    {% for item in items %}
                        <li>{{ item.name }} - ${{ item.price }}<br>
                            <small>Added on: {{ item.date_added }} at {{ item.time_added }}</small>
                        </li>
                    {% endfor %}
                </ul>
                <form action="/add" method="post">
                    <input type="text" name="name" placeholder="Item Name" required>
                    <input type="number" step="0.01" name="price" placeholder="Price" required>
                    <button type="submit">Add Item</button>
                </form>
                {% if error %}
                    <div class="error">{{ error }}</div>
                {% endif %}
            </div>
        </div>
    </body>
    </html>
    ''', items=items, error=request.args.get('error'))

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    price = request.form['price']
    
    if not name or not price:
        return redirect(url_for('index', error='All fields are required.'))
    
    try:
        price = float(price)
    except ValueError:
        return redirect(url_for('index', error='Invalid price format.'))

    new_item = MenuItem(name=name, price=price)
    db.session.add(new_item)
    db.session.commit()
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
