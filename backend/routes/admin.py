from flask import Blueprint, jsonify ,request
from flask_login import login_required, current_user
from models.models import db , Admin , ParkingLot , ParkingSpot , User , Reservation

admin_bp = Blueprint('admin', __name__)

def admin_required(func):
    @login_required
    def wrapper(*args, **kwargs):
        if not isinstance(current_user._get_current_object(), Admin):
            return jsonify({"error": "Unauthorized - Admins only"}), 403
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

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
    return jsonify({'message': 'Parking lot deleted'}), 200

@admin_bp.route('/lots/<int:lot_id>/spots', methods=['GET'])
@admin_required
def get_spots_of_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()

    result = [{
        'id': spot.id,
        'status': 'Available' if spot.status == 'A' else 'Occupied'
    } for spot in spots]

    return jsonify(result), 200

@admin_bp.route("/reservations", methods=["GET"])
@admin_required
def get_all_reservations():
    reservations = (
        Reservation.query
        .order_by(Reservation.parking_timestamp.desc())
        .limit(50)  # limit to latest 50 for performance
        .all()
    )
    data = []
    for r in reservations:
        data.append({
            "id": r.id,
            "user_id": r.user_id,
            "spot_id": r.spot_id,
            "lot_id": r.spot.lot_id if r.spot else None,
            "spot_number": r.spot.number if r.spot else None,
            "lot_name": r.spot.lot.name if r.spot and r.spot.lot else None,
            "parking_timestamp": r.parking_timestamp.isoformat(),
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