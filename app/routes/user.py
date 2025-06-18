from flask import Blueprint, jsonify, request
from ..models import User
from ..extensions import db, log, server_error
from ..middleware import admin_required

kurir_bp = Blueprint('kurir', __name__)

@kurir_bp.route('/', methods=['GET', 'POST'])
#@admin_required
def user():
    try:
        if request.method == 'GET':
            users = User.query.filter_by(role='kurir').all()
            user_list = [
                {
                    'id': user.id,
                    'nama': user.nama,
                    'email': user.email
                }
                for user in users
            ]

            response_data = {
                'status': 'success',
                'data': user_list
            }

            return jsonify(response_data), 200 
        
        if request.method == 'POST':
            data = request.json
            new_user = User(
                nama = data['nama'],
                email = data['email'],
                role = 'kurir'
            )
            new_user.set_password(data['password'])

            db.session.add(new_user)
            db.session.commit()

            user_data = {
                'id': new_user.id,
                'nama': new_user.nama,
                'email': new_user.email
            }

            response_data = {
                'status': 'success',
                'message': 'User berhasil ditambahkan.',
                'data': user_data
            }

            return jsonify(response_data), 201
        
    except Exception as e:
        log(str(e))

        if request.method == 'POST':
            db.session.rollback()

        return jsonify(server_error), 500