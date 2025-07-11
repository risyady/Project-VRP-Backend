from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    role = db.Column(db.Enum('admin', 'kurir', 'superadmin'), nullable=False)
    status = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    rute = db.relationship('Rute', backref='kurir', lazy=True, cascade="save-update, merge")

    def __repr__(self):
        return f'<User {self.nama}, ID: {self.id}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)