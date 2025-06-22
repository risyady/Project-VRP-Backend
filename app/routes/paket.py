from flask import Blueprint, jsonify, request
from ..extensions import db, server_error, log
from ..models import Paket
from ..middleware import kurir_required, admin_required

paket_bp = Blueprint('paket', __name__)

@paket_bp.route('/', methods=['GET', 'POST'])
#@admin_required
def paket():
    try:
        if request.method == 'GET':
            pakets = Paket.query.all()
            paket_list = [
                {
                    'id': paket.id,
                    'resi': paket.resi,
                    'nama_penerima': paket.nama_penerima,
                    'alamat': paket.alamat,
                    'no_penerima': paket.no_penerima,
                    'kuantitas': paket.kuantitas,
                    'deskripsi': paket.deskripsi,
                    'berat': paket.berat,
                    'status': paket.status
                }
                for paket in pakets
            ]

            response_data = {
                'status': 'success',
                'data': paket_list
            }

            return jsonify(response_data), 200
        
        if request.method == 'POST':
            data = request.json
            new_paket = Paket(
                nama_penerima = data.get('nama_penerima'),
                alamat = data.get('alamat'),
                no_penerima = data.get('no_penerima'),
                kuantitas = data.get('kuantitas'),
                deskripsi = data.get('deskripsi'),
                berat = data.get('berat'),
                status = 'di_gudang'
            )
            new_paket.set_coord(data.get('alamat'))

            if new_paket.latitude is None or new_paket.longitude is None:
                return jsonify({
                    'status': 'error',
                    'message': f'Tidak menemukan koordinat untuk alamat: {data.get("alamat")}'
                }), 400

            db.session.add(new_paket)
            db.session.commit()

            paket_data = {
                'id': new_paket.id,
                'resi': new_paket.resi,
                'nama_penerima': new_paket.nama_penerima,
                'alamat': new_paket.alamat,
                'no_penerima': new_paket.no_penerima,
                'kuantitas': new_paket.kuantitas,
                'deskripsi': new_paket.deskripsi,
                'berat': new_paket.berat,
                'status': new_paket.status
            }

            return jsonify({
                'status': 'success',
                'message': 'Paket berhasil ditambahkan.',
                'data': paket_data
            }), 201
    except Exception as e:
        log(str(e))
        if request.method == 'POST':
            db.session.rollback()
        return jsonify(server_error), 500