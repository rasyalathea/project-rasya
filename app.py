from flask import Flask, render_template, request, redirect, send_file
import mysql.connector
from fpdf import FPDF
from datetime import datetime
import os

app = Flask(__name__)

# Koneksi Database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_rawat_inap_rasyad"
)
cursor = db.cursor(dictionary=True)

# INDEX
@app.route("/")
def index():
    cursor.execute("""
        SELECT 
            t.id_transaksi_rasyad,
            p.nama_rasyad,
            k.kelas_rasyad AS status_kamar,
            r.tgl_masuk_rasyad,
            r.tgl_keluar_rasyad,
            t.total_biaya_rasyad,
            t.status_pembayaran_rasyad
        FROM transaksi_rasyad t
        JOIN pasien_rasyad p ON t.id_pasien_rasyad = p.id_pasien_rasyad
        LEFT JOIN rawat_inap_rasyad r ON t.id_rawat_rasyad = r.id_rawat_rasyad
        LEFT JOIN kamar_rasyad k ON r.id_kamar_rasyad = k.id_kamar_rasyad
    """)
    data = cursor.fetchall()
    return render_template("index_rasyad.html", data=data)

# TAMBAH TRANSAKSI
@app.route("/tambah", methods=["GET", "POST"])
def tambah():
    cursor.execute("SELECT id_pasien_rasyad, nama_rasyad FROM pasien_rasyad")
    pasien = cursor.fetchall()
    cursor.execute("""
        SELECT r.id_rawat_rasyad, r.id_pasien_rasyad, r.id_kamar_rasyad, 
               r.tgl_masuk_rasyad, r.tgl_keluar_rasyad, k.kelas_rasyad, k.status_kamar_rasyad
        FROM rawat_inap_rasyad r 
        JOIN kamar_rasyad k ON r.id_kamar_rasyad = k.id_kamar_rasyad
    """)
    rawat_inap = cursor.fetchall()

    if request.method == "POST":
        id_pasien = request.form["pasien"]

        # Jika tambah pasien baru
        if id_pasien == "tambah":
            nama_baru = request.form["nama_baru"]
            alamat_baru = request.form["alamat_baru"]
            kontak_baru = request.form["kontak_baru"]

            cursor.execute("""
                INSERT INTO pasien_rasyad (nama_rasyad, alamat_rasyad, kontak_rasyad)
                VALUES (%s, %s, %s)
            """, (nama_baru, alamat_baru, kontak_baru))
            db.commit()
            id_pasien = cursor.lastrowid

            # otomatis buat rawat inap baru untuk pasien ini
            cursor.execute("""
                INSERT INTO rawat_inap_rasyad (id_pasien_rasyad, id_kamar_rasyad, tgl_masuk_rasyad)
                VALUES (%s, NULL, %s)
            """, (id_pasien, datetime.now().date()))
            db.commit()

        id_rawat = request.form.get("rawat_inap")  # bisa kosong
        status = request.form["status"]
        tgl_masuk = request.form.get("tgl_masuk")
        tgl_keluar = request.form.get("tgl_keluar")

        total = 0

        if id_rawat:  # kalau pilih rawat inap
            cursor.execute("""
                UPDATE rawat_inap_rasyad SET
                    tgl_masuk_rasyad=%s,
                    tgl_keluar_rasyad=%s
                WHERE id_rawat_rasyad=%s
            """, (tgl_masuk, tgl_keluar if tgl_keluar else None, id_rawat))
            db.commit()

            cursor.execute("""
                SELECT tgl_masuk_rasyad, tgl_keluar_rasyad, id_kamar_rasyad 
                FROM rawat_inap_rasyad WHERE id_rawat_rasyad=%s
            """, (id_rawat,))
            rawat = cursor.fetchone()

            if rawat:
                masuk = datetime.strptime(str(rawat["tgl_masuk_rasyad"]), "%Y-%m-%d")
                keluar = datetime.strptime(str(rawat["tgl_keluar_rasyad"]), "%Y-%m-%d") if rawat["tgl_keluar_rasyad"] else masuk
                lama = max((keluar - masuk).days, 1)

                cursor.execute("SELECT harga_rasyad, status_kamar_rasyad FROM kamar_rasyad WHERE id_kamar_rasyad=%s", (rawat["id_kamar_rasyad"],))
                kamar = cursor.fetchone()

                if kamar and kamar["status_kamar_rasyad"] != "Terisi":
                    total = int(kamar["harga_rasyad"]) * lama
                else:
                    return "❌ Kamar sudah terisi!"

        # Insert transaksi (tanpa kolom tgl_rasyad, gunakan created_at otomatis)
        cursor.execute("""
            INSERT INTO transaksi_rasyad 
            (id_pasien_rasyad, id_rawat_rasyad, total_biaya_rasyad, status_pembayaran_rasyad)
            VALUES (%s, %s, %s, %s)
        """, (id_pasien, id_rawat if id_rawat else None, total, status))
        db.commit()
        return redirect("/")

    return render_template("form_rasyad.html", pasien=pasien, rawat_inap=rawat_inap)    

# EDIT TRANSAKSI
@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    # Ambil data pasien
    cursor.execute("SELECT id_pasien_rasyad, nama_rasyad FROM pasien_rasyad")
    pasien = cursor.fetchall()

    # Ambil data rawat inap + kamar
    cursor.execute("""
        SELECT r.id_rawat_rasyad, r.id_pasien_rasyad, r.id_kamar_rasyad, 
               r.tgl_masuk_rasyad, r.tgl_keluar_rasyad, k.kelas_rasyad, k.status_kamar_rasyad
        FROM rawat_inap_rasyad r 
        JOIN kamar_rasyad k ON r.id_kamar_rasyad = k.id_kamar_rasyad
    """)
    rawat_inap = cursor.fetchall()

    if request.method == "POST":
        id_pasien = request.form["pasien"]
        id_rawat = request.form["rawat_inap"]
        tgl_masuk = request.form["tgl_masuk"]
        tgl_keluar = request.form["tgl_keluar"]
        status = request.form["status"]

        # Hitung lama rawat inap
        masuk = datetime.strptime(tgl_masuk, "%Y-%m-%d")
        keluar = datetime.strptime(tgl_keluar, "%Y-%m-%d")
        lama = (keluar - masuk).days

        # Ambil harga kamar
        cursor.execute("SELECT harga_rasyad, status_kamar_rasyad FROM kamar_rasyad WHERE id_kamar_rasyad=%s", (id_rawat,))
        kamar = cursor.fetchone()
        if kamar["status_kamar_rasyad"] == "Terisi":
            return "❌ Kamar sudah terisi!"

        total = int(kamar["harga_rasyad"]) * lama

        # Update transaksi (tanpa tgl_masuk/keluar)
        cursor.execute("""
            UPDATE transaksi_rasyad SET
                id_pasien_rasyad=%s,
                id_rawat_rasyad=%s,
                total_biaya_rasyad=%s,
                status_pembayaran_rasyad=%s
            WHERE id_transaksi_rasyad=%s
        """, (id_pasien, id_rawat, total, status, id))

        # Update tanggal masuk/keluar di tabel rawat inap
        cursor.execute("""
            UPDATE rawat_inap_rasyad SET
                tgl_masuk_rasyad=%s,
                tgl_keluar_rasyad=%s
            WHERE id_rawat_rasyad=%s
        """, (tgl_masuk, tgl_keluar, id_rawat))

        db.commit()
        return redirect("/")

    cursor.execute("SELECT * FROM transaksi_rasyad WHERE id_transaksi_rasyad=%s", (id,))
    data = cursor.fetchone()
    return render_template("update_rasyad.html", data=data, pasien=pasien, rawat_inap=rawat_inap)


# DELETE
@app.route("/hapus/<id>")
def hapus(id):
    cursor.execute("DELETE FROM transaksi_rasyad WHERE id_transaksi_rasyad=%s", (id,))
    db.commit()
    return redirect("/")

# DATA PASIEN
@app.route("/pasien")
def pasien():
    cursor.execute("SELECT * FROM pasien_rasyad")
    data = cursor.fetchall()
    return render_template("pasien_rasyad.html", pasien=data)

# CETAK PDF PASIEN
@app.route("/cetak_pasien")
def cetak_pasien():
    cursor.execute("SELECT id_pasien_rasyad, nama_rasyad FROM pasien_rasyad")
    data = cursor.fetchall()

    class PDF(FPDF):
        def header(self):
            self.set_font('DejaVu', '', 16)
            self.set_text_color(30, 64, 175)
            self.cell(0, 10, "Laporan Data Pasien", ln=True, align='C')
            self.ln(2)
            self.set_draw_color(30, 64, 175)
            self.set_line_width(1)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(4)

        def footer(self):
            self.set_y(-15)
            self.set_font('DejaVu', '', 10)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, f'Halaman {self.page_no()}', align='C')

    pdf = PDF()
    # Tambahkan font SEBELUM add_page()
    pdf.add_font('DejaVu', '', os.path.join('fonts', 'DejaVuSans.ttf'), uni=True)
    pdf.set_font('DejaVu', '', 12)
    pdf.add_page()
    # Table header
    pdf.set_fill_color(30, 64, 175)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(40, 10, "ID Pasien", border=1, align='C', fill=True)
    pdf.cell(120, 10, "Nama Pasien", border=1, align='C', fill=True)
    pdf.ln()
    # Table body
    pdf.set_text_color(0, 0, 0)
    for row in data:
        pdf.cell(40, 10, str(row['id_pasien_rasyad']), border=1, align='C')
        pdf.cell(120, 10, row['nama_rasyad'], border=1)
        pdf.ln()
    pdf_path = "laporan_pasien.pdf"
    pdf.output(pdf_path)
    return send_file(pdf_path, as_attachment=True)

# CETAK LAPORAN SEMUA TRANSAKSI
@app.route("/cetak_transaksi")
def cetak_transaksi():
    cursor.execute("""
        SELECT 
            t.id_transaksi_rasyad,
            p.nama_rasyad,
            k.kelas_rasyad,
            r.tgl_masuk_rasyad,
            r.tgl_keluar_rasyad,
            t.total_biaya_rasyad,
            t.status_pembayaran_rasyad
        FROM transaksi_rasyad t
        JOIN pasien_rasyad p ON t.id_pasien_rasyad = p.id_pasien_rasyad
        JOIN rawat_inap_rasyad r ON t.id_rawat_rasyad = r.id_rawat_rasyad
        JOIN kamar_rasyad k ON r.id_kamar_rasyad = k.id_kamar_rasyad
    """)
    data = cursor.fetchall()

    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 14)
            self.cell(0, 10, "Laporan Transaksi Rawat Inap", ln=True, align='C')
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Halaman {self.page_no()}', align='C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # Header tabel
    pdf.set_fill_color(30, 64, 175)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(15, 8, "ID", border=1, align='C', fill=True)
    pdf.cell(35, 8, "Pasien", border=1, align='C', fill=True)
    pdf.cell(25, 8, "Kelas", border=1, align='C', fill=True)
    pdf.cell(25, 8, "Masuk", border=1, align='C', fill=True)
    pdf.cell(25, 8, "Keluar", border=1, align='C', fill=True)
    pdf.cell(30, 8, "Biaya", border=1, align='C', fill=True)
    pdf.cell(30, 8, "Status", border=1, align='C', fill=True)
    pdf.ln()

    # Isi tabel
    pdf.set_text_color(0, 0, 0)
    for row in data:
        pdf.cell(15, 8, str(row['id_transaksi_rasyad']), border=1, align='C')
        pdf.cell(35, 8, row['nama_rasyad'], border=1)
        pdf.cell(25, 8, row['kelas_rasyad'], border=1)
        pdf.cell(25, 8, str(row['tgl_masuk_rasyad']), border=1)
        pdf.cell(25, 8, str(row['tgl_keluar_rasyad']), border=1)
        pdf.cell(30, 8, f"Rp {int(row['total_biaya_rasyad']):,}", border=1)
        pdf.cell(30, 8, row['status_pembayaran_rasyad'], border=1)
        pdf.ln()

    pdf_path = "laporan_transaksi.pdf"
    pdf.output(pdf_path)
    return send_file(pdf_path, as_attachment=True)

# CETAK STRUK PER TRANSAKSI
@app.route("/cetak_struk/<id>")
def cetak_struk(id):
    cursor.execute("""
        SELECT 
            t.id_transaksi_rasyad,
            p.nama_rasyad,
            k.kelas_rasyad,
            r.tgl_masuk_rasyad,
            r.tgl_keluar_rasyad,
            t.total_biaya_rasyad,
            t.status_pembayaran_rasyad
        FROM transaksi_rasyad t
        JOIN pasien_rasyad p ON t.id_pasien_rasyad = p.id_pasien_rasyad
        JOIN rawat_inap_rasyad r ON t.id_rawat_rasyad = r.id_rawat_rasyad
        JOIN kamar_rasyad k ON r.id_kamar_rasyad = k.id_kamar_rasyad
        WHERE t.id_transaksi_rasyad=%s
    """, (id,))
    transaksi = cursor.fetchone()

    if not transaksi:
        return "❌ Transaksi tidak ditemukan!"

    pdf = FPDF('P', 'mm', (80, 150))  # ukuran kecil ala struk
    pdf.add_page()

    # Header
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 8, "Rumah Sakit Rasyad", ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 5, "Jl. Contoh No.123, Bandung", ln=True, align='C')
    pdf.cell(0, 5, "Telp: (021) 1234567", ln=True, align='C')
    pdf.ln(5)
    pdf.cell(0, 5, "=== STRUK PEMBAYARAN RAWAT INAP ===", ln=True, align='C')
    pdf.ln(5)

    # Isi
    pdf.set_font("Arial", '', 10)
    pdf.cell(35, 6, "ID Transaksi", 0, 0)
    pdf.cell(40, 6, f": {transaksi['id_transaksi_rasyad']}", 0, 1)
    pdf.cell(35, 6, "Nama Pasien", 0, 0)
    pdf.cell(40, 6, f": {transaksi['nama_rasyad']}", 0, 1)
    pdf.cell(35, 6, "Kelas Kamar", 0, 0)
    pdf.cell(40, 6, f": {transaksi['kelas_rasyad']}", 0, 1)
    pdf.cell(35, 6, "Tanggal Masuk", 0, 0)
    pdf.cell(40, 6, f": {transaksi['tgl_masuk_rasyad']}", 0, 1)
    pdf.cell(35, 6, "Tanggal Keluar", 0, 0)
    pdf.cell(40, 6, f": {transaksi['tgl_keluar_rasyad']}", 0, 1)
    pdf.cell(35, 6, "Total Biaya", 0, 0)
    pdf.cell(40, 6, f": Rp {int(transaksi['total_biaya_rasyad']):,}", 0, 1)
    pdf.cell(35, 6, "Status Bayar", 0, 0)
    pdf.cell(40, 6, f": {transaksi['status_pembayaran_rasyad']}", 0, 1)

    # Footer
    pdf.ln(10)
    pdf.cell(0, 5, "--------------------------------", ln=True, align='C')
    pdf.cell(0, 5, "Terima kasih atas kunjungan Anda", ln=True, align='C')
    pdf.cell(0, 5, "Semoga lekas sembuh 🙏", ln=True, align='C')

    pdf_path = f"struk_{id}.pdf"
    pdf.output(pdf_path)
    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
