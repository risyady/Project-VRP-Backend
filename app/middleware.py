from flask import session, jsonify
import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': 'Akses ditolak. Login terlebih dahulu'
            }), 401
        
        """ if session.get('role') != 'admin':
            return jsonify({
                'status': 'error',
                'message': 'Akses ditolak. Anda bukan admin.'
            }), 403 """
        
        return view(**kwargs)
    return wrapped_view

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': 'Akses ditolak. Login terlebih dahulu.'
            }), 401

        if session.get('role') != 'admin':
            return jsonify({
                'status': 'error',
                'message': 'Akses ditolak. Anda bukan admin.'
            }), 403
            
        return view(**kwargs)
    return wrapped_view

""" def kurir_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': 'Akses ditolak. Login terlebih dahulu.'
            }), 401

        if session.get('role') != 'kurir':
            return jsonify({
                'status': 'error',
                'message': 'Akses ditolak. Anda bukan kurir.'
            }), 403
            
        return view(**kwargs)
    return wrapped_view """