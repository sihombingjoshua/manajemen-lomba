import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# Impor library yang dibutuhkan untuk login
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# --- Konfigurasi Aplikasi ---
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Secret Key diperlukan untuk session management
app.config['SECRET_KEY'] = 'kunci-rahasia-yang-sangat-sulit-ditebak'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'competitions.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Konfigurasi Flask-Login ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Arahkan ke halaman 'login' jika user belum login

# --- Model Database ---

# Model User baru untuk login
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Model Kompetisi (tidak berubah)
class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    organizer = db.Column(db.String(100), nullable=False)
    registration_deadline = db.Column(db.Date, nullable=False)
    guidebook_link = db.Column(db.String(300))
    information_link = db.Column(db.String(300))
    status = db.Column(db.String(50), nullable=False, default='Submitted')
    submission_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Fungsi yang diperlukan oleh Flask-Login untuk mengambil data user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- Halaman & Logika (Routes) ---

# Halaman Utama (Dashboard) - SEKARANG DILINDUNGI
@app.route('/')
@login_required # Hanya user yang sudah login bisa mengakses ini
def index():
    all_competitions = Competition.query.order_by(Competition.submission_date.desc()).all()
    return render_template('index.html', competitions=all_competitions)

# --- HALAMAN BARU UNTUK OTENTIKASI ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Cek jika username sudah ada
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username sudah digunakan.', 'warning')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# --- ROUTE LAMA YANG SEKARANG DILINDUNGI ---

@app.route('/new', methods=['GET', 'POST'])
@login_required
def new_competition():
    if request.method == 'POST':
        # Mengambil data dari form
        name = request.form.get('name')
        organizer = request.form.get('organizer')
        deadline_str = request.form.get('deadline')
        guidebook_link = request.form.get('guidebook_link')
        information_link = request.form.get('information_link')

        # --- BLOK VALIDASI SISI SERVER ---
        if not name or not organizer or not deadline_str:
            flash('Nama, Penyelenggara, dan Deadline wajib diisi.', 'danger')
            # Kembali ke form jika ada data yang tidak valid
            return redirect(url_for('new_competition'))
        # --------------------------------

        # Jika validasi lolos, lanjutkan proses
        deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()

        new_comp = Competition(
            name=name,
            organizer=organizer,
            registration_deadline=deadline,
            guidebook_link=guidebook_link,
            information_link=information_link
        )
        db.session.add(new_comp)
        db.session.commit()
        flash('Kompetisi berhasil ditambahkan!', 'success')
        return redirect(url_for('index'))

    return render_template('new.html')
    
@app.route('/update_status/<int:id>', methods=['POST'])
@login_required # Melindungi fungsi update
def update_status(id):
    # Logika tidak berubah
    competition_to_update = Competition.query.get_or_404(id)
    competition_to_update.status = request.form['status']
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
@login_required # Melindungi fungsi delete
def delete_competition(id):
    # Logika tidak berubah
    competition_to_delete = Competition.query.get_or_404(id)
    db.session.delete(competition_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        # Sekarang create_all() akan membuat tabel User dan Competition
        db.create_all()
    app.run(debug=True)