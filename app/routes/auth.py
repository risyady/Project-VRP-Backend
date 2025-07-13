from flask import Blueprint, request, jsonify
from ..extensions import db, log, server_error
from ..models import User
from flask_jwt_extended import create_access_token, jwt_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({
                'status': 'error',
                'message': 'Email dan password harus diisi.'
            }), 400
        
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({
                'status': 'error',
                'message': 'Email atau password salah.'
            }), 401
        
        additional_claims = {'role': user.role, 'nama': user.nama}
        access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)

        return jsonify({
            'status': 'success',
            'message': 'Login berhasil.',
            'data': {
                'access_token': access_token,
                'user': {
                    'id': user.id,
                    'nama': user.nama,
                    'email': user.email,
                    'role': user.role
                }
            }
        }), 200
        
    except Exception as e:
        log(str(e))
        return jsonify(server_error), 500
    
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({
        'status': 'success', 
        'message': 'Anda telah berhasil logout.'
    }), 200
