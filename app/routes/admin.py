from flask import Blueprint, jsonify, request
from ..models import User
from ..extensions import db, log, server_error
from ..middleware import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/', methods=['GET', 'POST'])
#@admin_required
def admin():
    try:
        if request.method == 'GET':
            users = User.query.filter_by(role='admin').all()
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
                role = 'admin'
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
    
@admin_bp.route('/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def admin_detail(user_id):
    try:
        user = User.query.get_or_404(user_id)

        if request.method == 'GET':
            user_data = {
                'id': user.id,
                'nama': user.nama,
                'email': user.email,
                'role': user.role,
            }
            return jsonify({'status': 'success', 'data': user_data}), 200

        if request.method == 'PUT':
            data = request.json
            user.nama = data.get('nama', user.nama)
            user.email = data.get('email', user.email)
            if 'password' in data:
                user.set_password(data['password'])
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'User berhasil diperbarui.'}), 200

        if request.method == 'DELETE':
            db.session.delete(user)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'User berhasil dihapus.'}), 200

    except Exception as e:
        log(str(e))
        return jsonify(server_error), 500