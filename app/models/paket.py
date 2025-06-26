from ..extensions import db, get_coords
import datetime
import random

class Paket(db.Model):
    __tablename__ = 't_paket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resi = db.Column(db.String(100), unique=True, nullable=False)
    nama_penerima = db.Column(db.String(150), nullable=False)
    alamat = db.Column(db.Text)
    no_penerima = db.Column(db.String(20), nullable=False)
    latitude = db.Column(db.Double, nullable=False)
    longitude = db.Column(db.Double, nullable=False)
    kuantitas = db.Column(db.Integer, nullable=False)
    deskripsi = db.Column(db.Text)
    berat = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('di_gudang', 'dalam_pengiriman', 'berhasil', 'gagal'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    rute_detail = db.relationship('Rute_Detail', backref='paket', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<No. Resi {self.resi}>"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.resi:
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            random_number = random.randint(1000, 9999)
            self.resi = f"PDG-{timestamp}{random_number}"
    
    def set_coord(self, alamat):
        lat, lng = get_coords(alamat)
        self.latitude = lat
        self.longitude = lng