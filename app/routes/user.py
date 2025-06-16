from flask import Blueprint, jsonify, request
from ..models import User
from ..extensions import db, log, server_error

kurir_bp = Blueprint('kurir', __name__)

@kurir_bp.route('/', methods=['GET', 'POST'])
def kurir():
    try:
        if request.method == 'GET':
            kurirs = User.query.filter_by(role='kurir').all()
            kurir_list = [
                {
                    'id': kurir.id,
                    'nama': kurir.nama,
                    'email': kurir.email
                }
                for kurir in kurirs
            ]

            response_data = {
                'status': 'success',
                'data': kurir_list
            }

            return jsonify(response_data), 200 
        
        if request.method == 'POST':
            data = request.json
            new_kurir = User(
                nama = data['nama'],
                email = data['email'],
                role = 'kurir'
            )
            new_kurir.set_password(data['password'])

            db.session.add(new_kurir)
            db.session.commit()

            kurir_data = {
                'id': new_kurir.id,
                'nama': new_kurir.nama,
                'email': new_kurir.email
            }

            response_data = {
                'status': 'success',
                'message': 'User berhasil ditambahkan.',
                'data': kurir_data
            }

            return jsonify(response_data), 201
        
    except Exception as e:
        log(str(e))

        if request.method == 'POST':
            db.session.rollback()

        return jsonify(server_error), 500