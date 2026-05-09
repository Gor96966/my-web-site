import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# Բազայի միացում
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u_name = request.form.get('full_name')
        u_email = request.form.get('email')
        u_phone = request.form.get('phone')
        
        if u_name and u_email and u_phone:
            try:
                new_user = User(full_name=u_name, email=u_email, phone=u_phone)
                db.session.add(new_user)
                db.session.commit()
                return "<h1>Հաջողություն!</h1><a href='/'>Հետ դեպի գլխավոր</a>"
            except:
                db.session.rollback()
                return "<h1>Սխալ! Մեյլը արդեն կա:</h1>"
    return render_template('register.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
