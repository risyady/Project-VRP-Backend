from extensions import db

class Paket(db.Model):
    __tablename__ = 'pakets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resi = db.Column(db.String(50), unique=True, nullable=False)
    pengirim = db.Column(db.String(150), nullable=False)
    penerima = db.Column(db.String(150), nullable=False)
    alamat = db.Column(db.Text)
    no_pengirim = db.Column(db.String(20), nullable=False)
    no_penerima = db.Column(db.String(20), nullable=False)
    lat = db.Column(db.Double, nullable=False)
    lng = db.Column(db.Double, nullable=False)
    qty = db.Column(db.Integer)
    harga = db.Column(db.Integer)
    deskripsi = db.Column(db.Text)
    berat = db.Column(db.Double)
    batas_kirim = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('belum dikirim', 'dikirim', 'diterima'), nullable=False)

    def __repr__(self):
        return f"<No. Resi {self.resi}>"