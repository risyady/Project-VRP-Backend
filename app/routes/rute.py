from flask import Blueprint, request, jsonify, current_app
from ..extensions import db, server_error, log, vrp_solver
from ..models import Rute, Rute_Detail, Paket, User

rute_bp = Blueprint('rute', __name__)

@rute_bp.route('/optimasi-rute', methods=['POST'])
def create_rute():
    try:
        data = request.get_json(silent=True) or {}

        kurir_ids = data.get('kurir_ids')
        paket_ids = data.get('paket_ids')

        if kurir_ids:
            kurirs = User.query.filter(User.id.in_(kurir_ids), User.role == 'kurir').all()
            if len(kurirs) != len(kurir_ids):
                return jsonify({'status': 'error', 'message': 'Satu atau lebih ID kurir tidak valid.'}), 400
        else:
            kurirs = User.query.filter_by(role='kurir').all()

        if not kurirs:
            return jsonify({'status': 'error', 'message': 'Tidak ada kurir yang tersedia untuk optimasi.'}), 400

        if paket_ids:
            pakets = Paket.query.filter(Paket.id.in_(paket_ids), Paket.status == 'di_gudang').all()
            if len(pakets) != len(paket_ids):
                 return jsonify({'status': 'error', 'message': 'Satu atau lebih ID paket tidak valid atau statusnya bukan "di_gudang".'}), 400
        else:
            pakets = Paket.query.filter_by(status='di_gudang').all()
        
        if not pakets:
            return jsonify({'status': 'error', 'message': 'Tidak ada paket yang perlu dioptimasi.'}), 400

        depot_coords = current_app.config.get('DEPOT_COORDS')
        if not depot_coords:
            log("Error: DEPOT_COORDS tidak ditemukan di konfigurasi.")
            return jsonify(server_error), 500
        
        try:
            depot_coords = tuple(map(float,depot_coords.split(',')))
        except (ValueError, AttributeError):
            log(f"Error: Format DEPOT_COORDS tidak valid: {depot_coords}")
            return jsonify(server_error), 500

        # VRP
        vrp_response, status_code = vrp_solver(kurirs, pakets, depot_coords)
        
        return jsonify(vrp_response), status_code
    
    except Exception as e:
        db.session.rollback()
        log(f"Error di create_rute: {str(e)}")
        return jsonify(server_error), 500