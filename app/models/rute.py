from ..extensions import db

class Rute(db.Model):
    __tablename__ = 't_rute'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kurir_id = db.Column(db.Integer, db.ForeignKey('t_user.id'), nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)
    jarak_meter = db.Column(db.DECIMAL(10, 2), nullable=True)
    estimasi_detik = db.Column(db.Integer, nullable=True)
    waktu_berangkat = db.Column(db.TIMESTAMP, nullable=True)
    waktu_selesai = db.Column(db.TIMESTAMP, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    rute_detail = db.relationship('Rute_Detail', backref='rute', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ID pengiriman: {self.id}>"