to do:
- user submitter pada attribut submission
- sanitasi dan validasi input 

# Aplikasi Manajemen Submisi Lomba

Aplikasi web sederhana ini dikembangkan sebagai bagian dari tugas proyek untuk mengelola data submisi kompetisi. Fokus utama dari proyek ini adalah implementasi fitur-fitur keamanan dasar dalam lingkungan pengembangan lokal yang berjalan di atas protokol HTTPS.

## 🛠️ Teknologi yang Digunakan

  * **Backend:** Python 3
  * **Framework:** Flask
  * **Database:** SQLite via Flask-SQLAlchemy
  * **Otentikasi:** Flask-Login
  * **Keamanan:** Werkzeug Security (untuk password hashing)

## ✨ Fitur Utama

  * **Otentikasi Pengguna:** Sistem registrasi dan login yang aman.
  * **Manajemen Data (CRUD):** Pengguna yang sudah login dapat melakukan Create, Read, Update, dan Delete data kompetisi.
  * **Validasi Input:** Validasi ganda di sisi klien (browser) dan sisi server.
  * **HTTPS Lokal:** Aplikasi berjalan di lingkungan `localhost` yang aman menggunakan sertifikat SSL/TLS.
  * **Keamanan:** Menerapkan prinsip-prinsip *secure coding* seperti *hashing password* dan pembatasan hak akses.

-----

## 🚀 Cara Menjalankan Aplikasi

Berikut adalah langkah-langkah untuk menyiapkan dan menjalankan aplikasi ini di lingkungan lokal.

### 1\. Prasyarat

  * Python 3.8 atau versi lebih baru.
  * `pip` (package installer for Python).
  * `git` (untuk kloning repositori).
  * `openssl` (untuk membuat sertifikat, biasanya sudah terpasang di Linux/macOS).

### 2\. Instalasi

1.  **Kloning Repositori**
    Buka terminal dan jalankan perintah berikut:

    ```bash
    git clone https://github.com/sihombingjoshua/manajemen-lomba.git
    cd manajemen-lomba
    ```

2.  **Buat Virtual Environment** (Sangat disarankan)

    ```bash
    python -m venv venv
    source venv/bin/activate  # Di Windows: venv\Scripts\activate
    ```

3.  **Instal Dependensi**
    Instal semua library yang dibutuhkan dari file `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```


### 3\. Konfigurasi HTTPS

Aplikasi ini wajib berjalan di atas HTTPS. Lakukan langkah-langkah di bagian **Konfigurasi HTTPS** di bawah untuk membuat file sertifikat anda sendiri.

### 4\. Jalankan Aplikasi

Setelah sertifikat dibuat dan semua dependensi terinstal, jalankan server Flask:

```bash
python app.py
```

Aplikasi sekarang akan berjalan dan dapat diakses melalui **`https://127.0.0.1:5000`**.

-----

## 🔐 Konfigurasi HTTPS

Untuk mengaktifkan HTTPS di `localhost`, kita menggunakan sertifikat yang ditandatangani sendiri (*self-signed certificate*) yang dibuat dengan **OpenSSL**.

1.  **Buat Sertifikat**
    Masuk ke dalam folder cert/, jika tidak ada anda dapat membuatnya, lalu jalankan perintah berikut di terminal:

    ```bash
    openssl req -x509 -newkey rsa:4096 -nodes -keyout key.pem -out cert.pem -days 365
    ```

    Perintah ini akan menghasilkan dua file: `key.pem` (kunci privat) dan `cert.pem` (sertifikat publik).

2.  **Integrasi dengan Flask**
    Di dalam file `app.py`, server dijalankan dengan menyertakan `ssl_context` yang mengarah ke file-file tersebut:

    ```python
    if __name__ == '__main__':
        # ... (kode lain) ...
        app.run(debug=True, ssl_context=('cert/cert.pem', 'cert/key.pem'))
    ```

⚠️ **Peringatan Browser**
Saat pertama kali mengakses `https://127.0.0.1:5000`, browser akan menampilkan peringatan keamanan. Ini normal karena sertifikat kita tidak dikeluarkan oleh otoritas tepercaya. Klik "Advanced" -\> "Proceed to 127.0.0.1 (unsafe)" untuk melanjutkan.

-----

## 🛡️ Implementasi Keamanan

Aplikasi ini menerapkan beberapa prinsip *secure coding* yang fundamental.

### 1\. Validasi Input (Input Validation)

Validasi diterapkan di dua lapisan untuk memastikan integritas data:

  * **Sisi Klien:** Menggunakan atribut HTML5 seperti `required`, `type="date"`, dan `type="url"` pada form untuk memberikan umpan balik cepat kepada pengguna.
  * **Sisi Server:** Sebelum data disimpan ke database, kode di `app.py` memeriksa apakah input-input penting (seperti nama dan penyelenggara) tidak kosong. Ini mencegah data yang tidak valid masuk ke sistem meskipun validasi klien dilewati.

### 2\. Password Hashing

Password pengguna **tidak pernah** disimpan dalam bentuk teks biasa.

  * **Implementasi:** Menggunakan library `werkzeug.security`.
  * **Pendaftaran:** Saat pengguna mendaftar, password mereka diubah menjadi *hash* menggunakan `generate_password_hash()`.
  * **Login:** Saat login, password yang diinput akan di-*hash* kembali dan dibandingkan dengan *hash* yang tersimpan di database menggunakan `check_password_hash()`. Proses ini bersifat satu arah dan aman.

### 3\. Pembatasan Hak Akses (Access Control)

Fitur-fitur sensitif seperti membuat, mengubah, dan menghapus data dilindungi agar hanya bisa diakses oleh pengguna yang sudah login.

  * **Implementasi:** Menggunakan *decorator* `@login_required` dari library `Flask-Login`.
  * **Mekanisme:** Setiap *route* yang diberi *decorator* ini akan secara otomatis memeriksa apakah ada sesi pengguna yang aktif. Jika tidak, pengguna akan diarahkan ke halaman login.

### 4\. Manajemen Sesi Aman (Secure Session Management)

Untuk mendapatkan **nilai plus**, mekanisme sesi ditangani dengan aman.

  * **Implementasi:** Library `Flask-Login` menangani sesi pengguna secara otomatis.
  * **Mekanisme:** `Flask-Login` membuat *cookie* sesi yang ditandatangani secara kriptografis menggunakan `SECRET_KEY` yang diatur di konfigurasi aplikasi. Ini mencegah *cookie* dimanipulasi oleh pengguna.

-----

## 👨‍💻 Anggota Kelompok

1.  Joshua Pratama Sihombing - 2322101929
2.  Hafizhah Luthfi Abdillah - 2322101914
3.  Fairus Febrian Rahardiyana Putra - 2322101902
4.  Anggel Marya Savrila - 2232101879