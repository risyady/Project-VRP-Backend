from flask import Blueprint, request, jsonify, current_app
from ..extensions import db, server_error, log, vrp_solver
from ..models import Rute, Rute_Detail, Paket, User
from sqlalchemy.orm import joinedload

rute_bp = Blueprint('rute', __name__)

@rute_bp.route('/', methods=['GET'])
def get_all_rute():
    try:
        rutes = Rute.query.options(
            joinedload(Rute.kurir),
            joinedload(Rute.rute_detail).joinedload(Rute_Detail.paket)
        ).order_by(Rute.created_at.desc()).all()

        rute_list = [
            {
                'id': rute.id,
                'kurir': rute.kurir.nama,
                'created_at': rute.created_at.isoformat(),
                'estimasi': rute.get_estimation_in_complete_time(),
                'jarak': rute.jarak_meter,
                'status': rute.status,
                'rute_detail': [
                    {
                        'id': detail.id,
                        'urutan': detail.urutan,
                        'waktu_tiba': detail.waktu_tiba.isoformat() if detail.waktu_tiba else None,
                        'paket': {
                            'id': detail.paket.id,
                            'resi': detail.paket.resi,
                            'nama_penerima': detail.paket.nama_penerima,
                            'alamat': detail.paket.alamat,
                            'status': detail.paket.status
                        }
                    }
                    for detail in sorted(rute.rute_detail, key=lambda d: d.urutan)
                ]
            }
            for rute in rutes
        ]

        response_data = {
            'status': 'success',
            'data': rute_list
        }

        return jsonify(response_data), 200
    except Exception as e:
        db.session.rollback()
        log(f"Error di get_all_rute: {str(e)}")
        return jsonify(server_error), 500

@rute_bp.route('/<int:id>', methods=['GET'])
def get_rute_by_id(id):
    try:
        rute = Rute.query.options(
            joinedload(Rute.kurir),
            joinedload(Rute.rute_detail).joinedload(Rute_Detail.paket)
        ).filter_by(id=id).first_or_404(description=f"Rute dengan ID {id} tidak ditemukan.")

        rute_data = {
            'id': rute.id,
            'kurir': rute.kurir.nama,
            'created_at': rute.created_at.isoformat(),
            'estimasi': rute.get_estimation_in_complete_time(),
            'jarak': rute.jarak_meter,
            'status': rute.status,
            'polyline': rute.polyline,
            'rute_detail': [
                {
                    'id': detail.id,
                    'urutan': detail.urutan,
                    'waktu_tiba': detail.waktu_tiba.isoformat() if detail.waktu_tiba else None,
                    'paket': {
                        'id': detail.paket.id,
                        'resi': detail.paket.resi,
                        'nama_penerima': detail.paket.nama_penerima,
                        'alamat': detail.paket.alamat,
                        'status': detail.paket.status
                    }
                }
                for detail in sorted(rute.rute_detail, key=lambda d: d.urutan)
            ]
        }
        return jsonify({'status': 'success', 'data': rute_data}), 200
    except Exception as e:
        log(f"Error di get_rute_by_id: {str(e)}")
        return jsonify(server_error), 500

@rute_bp.route('/optimasi', methods=['GET', 'POST'])
def create_rute():
    try:
        if request.method == 'GET':
            kurirs = User.query.with_entities(User.id, User.nama).filter_by(role='kurir', status=True).all()
            pakets = Paket.query.with_entities(Paket.id, Paket.resi, Paket.alamat).filter_by(status='di_gudang').all()

            paket_list = [
                {
                    'id': paket.id,
                    'resi': paket.resi,
                    'alamat': paket.alamat
                }
                for paket in pakets
            ]

            kurir_list = [
                {
                    'id': kurir.id,
                    'nama': kurir.nama
                }
                for kurir in kurirs
            ]

            response_data = {
                'status': 'success',
                'data': {
                    'kurirs': kurir_list,
                    'pakets': paket_list
                }
            }

            return jsonify(response_data), 200

        if request.method == 'POST':
            data = request.get_json(silent=True) or {}       

            kurir_ids = data.get('kurir_ids')
            paket_ids = data.get('paket_ids')

            kurirs = User.query.filter(User.id.in_(kurir_ids), User.role == 'kurir', User.status == True).all()
            pakets = Paket.query.filter(Paket.id.in_(paket_ids), Paket.status == 'di_gudang').all()

            """ if kurir_ids:
                kurirs = User.query.filter(User.id.in_(kurir_ids), User.role == 'kurir').all()
                if len(kurirs) != len(kurir_ids):
                    return jsonify({'status': 'error', 'message': 'Satu atau lebih ID kurir tidak valid.'}), 400
            else:
                kurirs = User.query.filter_by(role='kurir').all() """

            if not kurirs:
                return jsonify({'status': 'error', 'message': 'Tidak ada kurir yang tersedia untuk optimasi.'}), 400

            """ if paket_ids:
                pakets = Paket.query.filter(Paket.id.in_(paket_ids), Paket.status == 'di_gudang').all()
                if len(pakets) != len(paket_ids):
                    return jsonify({'status': 'error', 'message': 'Satu atau lebih ID paket tidak valid atau statusnya bukan "di_gudang".'}), 400
            else:
                pakets = Paket.query.filter_by(status='di_gudang').all() """
            
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

            """ response_data = {
                'status': 'success',
                'data': vrp_response
            }

            return jsonify(response_data), status_code """

            if status_code != 200:
                return jsonify(vrp_response), status_code
            
            solution = vrp_response.get('solution')
            if not solution:
                return jsonify({'status': 'error', 'message': 'Solusi rute tidak ditemukan dalam respons VRP.'}), 400
            
            try:

                created_rute_ids = []
                assigned_kurir_ids = []

                for route in solution['routes']:
                    kurir_id = int(route['vehicle_id'])
                    assigned_kurir_ids.append(kurir_id)
                    
                    new_rute = Rute(
                        kurir_id=kurir_id,
                        jarak_meter=route.get('distance'),
                        estimasi_detik=route.get('completion_time'),
                        polyline=route.get('points')
                    )
                    db.session.add(new_rute)
                    db.session.flush()

                    for i, activity in enumerate(route['activities'], 0):
                        if activity['type'] == 'service':
                            paket_id = int(activity['id'])

                            rute_detail = Rute_Detail(
                                rute_id=new_rute.id,
                                paket_id=paket_id,
                                urutan=i
                            )
                            db.session.add(rute_detail)

                    created_rute_ids.append(new_rute.id)

                Paket.query.filter(Paket.id.in_(paket_ids)).update({'status': 'dalam_pengiriman'}, synchronize_session=False)
                User.query.filter(User.id.in_(assigned_kurir_ids)).update({'status': False}, synchronize_session=False)

                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Rute berhasil dioptimasi dan disimpan.', 'rute_ids': created_rute_ids}), 201

            except Exception as e:
                db.session.rollback()
                log(f"Error saat menyimpan rute ke DB: {str(e)}")
                return jsonify(server_error), 500
                
    except Exception as e:
        db.session.rollback()
        log(f"Error di create_rute: {str(e)}")
        return jsonify(server_error), 500