import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# --- Konfigurasi Aplikasi ---
app = Flask(__name__)
# Menentukan path absolut untuk database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'competitions.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Model Database ---
# Mendefinisikan struktur tabel untuk kompetisi
class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    organizer = db.Column(db.String(100), nullable=False)
    registration_deadline = db.Column(db.Date, nullable=False)
    guidebook_link = db.Column(db.String(300))
    information_link = db.Column(db.String(300))
    status = db.Column(db.String(50), nullable=False, default='Submitted') # Status default
    submission_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Competition {self.name}>'

# --- Halaman & Logika (Routes) ---

# Halaman Utama (Dashboard) - READ
@app.route('/')
def index():
    # Mengambil semua data kompetisi dari DB dan mengurutkannya
    all_competitions = Competition.query.order_by(Competition.submission_date.desc()).all()
    return render_template('index.html', competitions=all_competitions)

# Halaman untuk menambah kompetisi baru - CREATE
@app.route('/new', methods=['GET', 'POST'])
def new_competition():
    if request.method == 'POST':
        # Mengambil data dari form
        name = request.form['name']
        organizer = request.form['organizer']
        deadline_str = request.form['deadline']
        deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        guidebook_link = request.form['guidebook_link']
        information_link = request.form['information_link']

        # Membuat objek kompetisi baru
        new_comp = Competition(
            name=name,
            organizer=organizer,
            registration_deadline=deadline,
            guidebook_link=guidebook_link,
            information_link=information_link
        )

        # Menyimpan ke database
        try:
            db.session.add(new_comp)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "Terjadi kesalahan saat menyimpan data."

    return render_template('new.html')

# Logika untuk mengupdate status - UPDATE
@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    competition_to_update = Competition.query.get_or_404(id)
    new_status = request.form['status']
    competition_to_update.status = new_status
    try:
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "Terjadi kesalahan saat mengupdate status."

# Logika untuk menghapus data - DELETE
@app.route('/delete/<int:id>', methods=['POST'])
def delete_competition(id):
    competition_to_delete = Competition.query.get_or_404(id)
    try:
        db.session.delete(competition_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "Terjadi kesalahan saat menghapus data."


if __name__ == '__main__':
    # Baris ini memastikan create_all() hanya dijalankan sekali jika DB belum ada
    with app.app_context():
        db.create_all()
    app.run(debug=True)