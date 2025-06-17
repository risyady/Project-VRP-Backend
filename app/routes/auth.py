from flask import Blueprint, request, jsonify, session
from ..extensions import db, log, server_error
from ..models import User
from ..middleware import login_required

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
        
        session.clear()
        session['user_id'] = user.id
        session['nama'] = user.nama
        session['role'] = user.role
        
        return jsonify({
            'status': 'success',
            'message': 'Login berhasil.',
            'data': {
                'user_id': user.id,
                'nama': user.nama,
                'role': user.role
            }
        }), 200
        
    except Exception as e:
        log(str(e))
        return jsonify(server_error), 500
    
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    return jsonify({
        'status': 'success', 
        'message': 'Anda telah berhasil logout.'
    }), 200
