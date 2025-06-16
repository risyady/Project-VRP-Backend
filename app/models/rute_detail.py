from ..extensions import db

class Rute_Detail(db.Model):
    __tablename__ = 't_rute_detail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rute_id = db.Column(db.Integer, db.ForeignKey('t_rute.id'), nullable=False)
    paket_id = db.Column(db.Integer, db.ForeignKey('t_paket.id'), nullable=False)
    urutan = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Paket: {self.paket_id}, Rute ke: {self.rute_id}, Urutan ke: {self.urutan}"