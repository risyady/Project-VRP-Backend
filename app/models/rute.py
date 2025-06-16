from ..extensions import db

class Rute(db.Model):
    __tablename__ = 't_rute'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kurir_id = db.Column(db.Integer, db.ForeignKey('t_user.id'), nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    rute_detail = db.relationship('Rute_Detail', backref='rute', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ID pengiriman: {self.id}>"