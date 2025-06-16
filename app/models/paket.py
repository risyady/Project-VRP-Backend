from ..extensions import db

class Paket(db.Model):
    __tablename__ = 't_paket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resi = db.Column(db.String(50), unique=True, nullable=False)
    pengirim = db.Column(db.String(150), nullable=False)
    penerima = db.Column(db.String(150), nullable=False)
    alamat = db.Column(db.Text)
    no_pengirim = db.Column(db.String(20), nullable=False)
    no_penerima = db.Column(db.String(20), nullable=False)
    lat = db.Column(db.Double, nullable=False)
    lng = db.Column(db.Double, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    deskripsi = db.Column(db.Text)
    berat = db.Column(db.Double, nullable=False)
    batas_kirim = db.Column(db.Date, nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    rute_detail = db.relationship('Rute_Detail', backref='paket', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<No. Resi {self.resi}>"