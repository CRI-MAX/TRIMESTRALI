from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    clienti = Cliente.query.all()
    return render_template('index.html', clienti=clienti)

if __name__ == '__main__':
    app.run(debug=True)