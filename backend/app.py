import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

app = Flask(__name__, template_folder='/app/templates', static_folder='/app/static')
app.config['SECRET_KEY'] = 'synergy-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='admin@synergy.it').first():
            pw = generate_password_hash('admin123', method='pbkdf2:sha256')
            admin = User(username='Eddy Pasquale Chiacchio', email='admin@synergy.it', password=pw, role='Admin')
            db.session.add(admin)
            db.session.commit()

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
