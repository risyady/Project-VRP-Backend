from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity
from ..models import User
from ..extensions import db, log, server_error
from ..middleware import jwt_required, role_required

kurir_bp = Blueprint('kurir', __name__)

@kurir_bp.route('/', methods=['GET'])
@role_required('admin', 'superadmin')
def user():
    try:   
        users = User.query.filter_by(role='kurir').all()
        user_list = [
            {
                'id': user.id,
                'nama': user.nama,
                'email': user.email,
                'status': user.status
            }
            for user in users
        ]

        response_data = {
            'status': 'success',
            'data': user_list
        }

        return jsonify(response_data), 200 
        
    except Exception as e:
        log(str(e))
        return jsonify(server_error), 500
    
@kurir_bp.route('/', methods=['POST'])
@role_required('admin')
def add_user():
    try:
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
        db.session.rollback()
        return jsonify(server_error), 500
    
@kurir_bp.route('/<int:user_id>', methods=['PUT', 'DELETE'])
@role_required('admin')
def user_detail(user_id):
    try:
        user = User.query.get_or_404(user_id)

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
    
@kurir_bp.route('/me', methods=['GET', 'PUT'])
@jwt_required()
def me():
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        if request.method == 'GET':
            user_data = {
                'id': user.id,
                'nama': user.nama,
                'email': user.email,
                'role': user.role,
            }

            if user.role == 'kurir':
                user_data['status'] = user.status

            return jsonify({'status': 'success', 'data': user_data}), 200

        if request.method == 'PUT':
            data = request.json
            user.nama = data.get('nama', user.nama)
            user.email = data.get('email', user.email)
            if 'password' in data:
                user.set_password(data['password'])
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Profil berhasil diperbarui.'}), 200

    except Exception as e:
        log(str(e))
        return jsonify(server_error), 500