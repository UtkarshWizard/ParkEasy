from flask import Blueprint, jsonify ,request
from models.models import db , ParkingLot , ParkingSpot , User , Reservation
from utils.decorators import admin_required
from utils.extension import cache

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def admin_dashboard():
    return jsonify({"message": "Welcome to the Admin Dashboard"})

@admin_bp.route('/lots', methods=['POST'])
@admin_required
def create_parking_lot():
    data = request.json
    location_name = data.get('location_name')
    price_per_hour = data.get('price_per_hour')
    address = data.get('address')
    pincode = data.get('pincode')
    no_of_spots = data.get('no_of_spots')

    if not all([location_name, price_per_hour, address, pincode, no_of_spots]):
        return jsonify({'error': 'Missing required fields'}), 400

    new_lot = ParkingLot(
        location_name=location_name,
        price_per_hour=price_per_hour,
        address=address,
        pincode=pincode,
        no_of_spots=no_of_spots
    )
    db.session.add(new_lot)
    db.session.commit()

    for _ in range(no_of_spots):
        spot = ParkingSpot(lot_id=new_lot.id, status='A')
        db.session.add(spot)

    db.session.commit()

    return jsonify({'message': 'Parking lot created successfully'}), 201

@admin_bp.route('/lots', methods=['GET'])
@admin_required
@cache.cached(timeout=60, key_prefix="admin_all_lots")
def get_parking_lots():
    lots = ParkingLot.query.all()
    result = []
    for lot in lots:
        total_spots = len(lot.spots)
        occupied_spots = sum(1 for spot in lot.spots if spot.status == "O")

        result.append({
            'id': lot.id,
            'location_name': lot.location_name,
            'price_per_hour': lot.price_per_hour,
            'address': lot.address,
            'pincode': lot.pincode,
            'no_of_spots': total_spots,
            "occupied_spots" : occupied_spots
        })
    return jsonify(result), 200

@admin_bp.route('/lots/<int:lot_id>', methods=['PUT'])
@admin_required
def update_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    data = request.json

    lot.location_name = data.get('location_name', lot.location_name)
    lot.price_per_hour = data.get('price_per_hour', lot.price_per_hour)
    lot.address = data.get('address', lot.address)
    lot.pincode = data.get('pincode', lot.pincode)
    lot.no_of_spots = data.get('no_of_spots' , lot.no_of_spots)

    db.session.commit()

    cache.delete("admin_all_lots")
    return jsonify({'message': 'Parking lot updated'}), 200

@admin_bp.route('/lots/<int:lot_id>', methods=['DELETE'])
@admin_required
def delete_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)

    for spot in lot.spots:
        for reservation in spot.reservations:
            db.session.delete(reservation)
        db.session.delete(spot)

    db.session.delete(lot)
    db.session.commit()

    cache.delete("admin_all_lots")
    cache.delete(f"lot_spots_{lot_id}")
    return jsonify({'message': 'Parking lot deleted'}), 200

@admin_bp.route('/lots/<int:lot_id>/spots', methods=['GET'])
@admin_required
@cache.cached(timeout=60, key_prefix=lambda: f"lot_spots_{request.view_args['lot_id']}")
def get_spots_of_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()

    result = []
    for spot in spots:
        current_reservation = Reservation.query.filter_by(
            spot_id=spot.id,
            leaving_timestamp=None
        ).first()

        user_info = None
        start_time = None
        if current_reservation:
            user_info = {
                "fullname": current_reservation.user.fullname,
                "email": current_reservation.user.email
            }
            start_time = current_reservation.parking_timestamp.isoformat() if current_reservation.parking_timestamp else None

        result.append({
            'id': spot.id,
            'status': 'Available' if spot.status == 'A' else 'Occupied',
            'user': user_info,
            'start_time': start_time
        })

    return jsonify(result), 200

@admin_bp.route("/reservations", methods=["GET"])
@admin_required
def get_all_reservations():
    reservations = (
        Reservation.query
        .order_by(Reservation.parking_timestamp.desc())
        .limit(50)
        .all()
    )
    data = []
    for r in reservations:
        data.append({
            "id": r.id,
            "user_id": r.user_id,
            "spot_id": r.spot_id,
            "lot_id": r.spot.lot_id if r.spot else None,
            "spot_number": r.spot.id if r.spot else None,
            "lot_name": r.spot.lot.location_name if r.spot and r.spot.lot else None,
            "booking_timestamp" : r.booking_timestamp.isoformat(),
            "parking_timestamp": r.parking_timestamp.isoformat() if r.parking_timestamp else None,
            "leaving_timestamp": r.leaving_timestamp.isoformat() if r.leaving_timestamp else None,
            "parking_cost": r.parking_cost,
        })
    return jsonify(data)

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        reservations = Reservation.query.filter_by(user_id=user.id).all()
        active_res = [r for r in reservations if r.leaving_timestamp is None]
        result.append({
            'fullname': user.fullname,
            'email': user.email,
            'active_reservations': len(active_res),
        })
    return jsonify(result), 200

@admin_bp.route('/analytics/revenue', methods=['GET'])
@admin_required
@cache.cached(timeout=300, key_prefix="analytics_revenue")
def revenue_per_lot():
    lots = ParkingLot.query.all()
    data = []
    for lot in lots:
        total = sum(r.parking_cost for spot in lot.spots for r in spot.reservations if r.parking_cost)
        data.append({'lot': lot.location_name, 'revenue': total})
    return jsonify(data)

@admin_bp.route('/analytics/occupancy', methods=['GET'])
@admin_required
@cache.cached(timeout=60, key_prefix="analytics_occupancy")
def occupancy_per_lot():
    lots = ParkingLot.query.all()
    data = []
    for lot in lots:
        available = sum(1 for spot in lot.spots if spot.status == 'A')
        occupied = sum(1 for spot in lot.spots if spot.status == 'O')
        data.append({
            'lot': lot.location_name,
            'available': available,
            'occupied': occupied
        })
    return jsonify(data)

@admin_bp.route('/analytics/average-duration', methods=['GET'])
@admin_required
@cache.cached(timeout=300, key_prefix="analytics_avg_duration")
def avg_duration_per_lot():
    lots = ParkingLot.query.all()
    data = []
    for lot in lots:
        durations = []
        for spot in lot.spots:
            for r in spot.reservations:
                if r.parking_timestamp and r.leaving_timestamp:
                    duration = (r.leaving_timestamp - r.parking_timestamp).total_seconds() / 3600
                    durations.append(duration)
        avg = round(sum(durations) / len(durations), 2) if durations else 0
        data.append({'lot': lot.location_name, 'avg_duration': avg})
    return jsonify(data)
