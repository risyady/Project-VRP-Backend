from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity
from ..extensions import db, server_error, log
from ..models import Paket, Rute, Rute_Detail, User
from ..middleware import jwt_required
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)

def format_duration(seconds):
    if not seconds or seconds < 0:
        return '0 jam 0 menit'

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)

    return f'{hours} jam {minutes} menit'

@dashboard_bp.route('/', methods=['GET'])
@jwt_required()
def get_stats():
    try:
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        user_role = claims.get('role')

        stats = {}

        if user_role in ['admin', 'superadmin']:
            stats['total_paket'] = db.session.query(Paket.id).count()
            stats['paket_terkirim'] = db.session.query(Paket.id).filter(Paket.status == 'berhasil').count()
            stats['paket_di_gudang'] = db.session.query(Paket.id).filter(Paket.status == 'di_gudang').count()
            stats['paket_dalam_pengiriman'] = db.session.query(Paket.id).filter(Paket.status == 'dalam_pengiriman').count()
            stats['total_kurir'] = db.session.query(User.id).filter(User.role == 'kurir').count()
            stats['kurir_tersedia'] = db.session.query(User.id).filter(User.role == 'kurir', User.status == True).count()
            stats['total_rute'] = db.session.query(Rute.id).count()
            stats['rute_selesai'] = db.session.query(Rute.id).filter(Rute.status == True).count()
            if user_role == 'superadmin':
                stats['total_admin'] = db.session.query(User.id).filter(User.role == 'admin').count()

        elif user_role == 'kurir':
            stats['kurir_paket_dikirim'] = db.session.query(Paket.id).join(Rute_Detail, Paket.id == Rute_Detail.paket_id).join(Rute, Rute_Detail.rute_id == Rute.id).filter(Rute.kurir_id == current_user_id, Paket.status == 'berhasil').count()
            stats['kurir_rute_diselesaikan'] = db.session.query(Rute.id).filter(Rute.kurir_id == current_user_id, Rute.status == True).count()
            total_seconds = db.session.query(func.sum(Rute.estimasi_detik)).filter(Rute.kurir_id == current_user_id, Rute.status == True).scalar()
            stats['kurir_estimasi_waktu_total'] = format_duration(total_seconds or 0)

        response_data = {
            'status': 'success',
            'data': stats
        }

        return jsonify(response_data), 200

    except Exception as e:
        log(f'Error di dashboard.get_stats: {str(e)}')
        return jsonify(server_error), 500