from flask import Blueprint , jsonify;
from flask_login import login_required , current_user;
from datetime import datetime , timezone;
from models.models import db, ParkingLot, ParkingSpot, Reservation;
from utils.decorators import user_required;

user_bp = Blueprint('user' , __name__);

@user_bp.route('/lots' , methods=['GET'])
@user_required
def get_available_spots():
    lots = ParkingLot.query.all()
    result = []
    for lot in lots:
        available_spots = ParkingSpot.query.filter_by(lot_id = lot.id , status='A').count()
        result.append({
            "id" : lot.id,
            "location_name" : lot.location_name,
            "address" : lot.address,
            "pincode" : lot.pincode,
            "price_per_hour" : lot.price_per_hour,
            "available_spots" : available_spots,
            "total_spots" : lot.no_of_spots
        })
    return jsonify(result), 200
    
@user_bp.route('/reserve/<int:lot_id>', methods=['POST'])
@user_required
def reserve_spot(lot_id):
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not spot:
        return jsonify({"error": "No available spots"}), 404

    spot.status = 'O'
    reservation = Reservation(
        spot_id=spot.id,
        user_id=current_user.id,
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify({"message": "Spot reserved", "spot_id": spot.id, "reservation_id": reservation.id}), 200

@user_bp.route('/occupy/<int:reservation_id>', methods=['POST'])
@user_required
def occupy_spot(reservation_id):
    reservation = Reservation.query.filter_by(id=reservation_id, user_id=current_user.id).first()
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404

    reservation.parking_timestamp = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify({"message": "Occupy timestamp updated"}), 200

@user_bp.route('/release/<int:reservation_id>', methods=['POST'])
@user_required
def release_spot(reservation_id):
    reservation = Reservation.query.filter_by(id=reservation_id, user_id=current_user.id).first()
    if not reservation or reservation.leaving_timestamp is not None:
        return jsonify({"error": "Invalid or already released"}), 400

    reservation.leaving_timestamp = datetime.now(timezone.utc)
    spot = ParkingSpot.query.get(reservation.spot_id)
    lot = ParkingLot.query.get(spot.lot_id)

    start_time = reservation.booking_timestamp
    end_time = reservation.leaving_timestamp

    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)
    if end_time.tzinfo is None:
        end_time = end_time.replace(tzinfo=timezone.utc)

    duration_hours = max((end_time - start_time).total_seconds() / 3600, 1)
    reservation.parking_cost = round(duration_hours * lot.price_per_hour, 2)

    spot.status = 'A'

    db.session.commit()
    return jsonify({"message": "Spot released", "cost": reservation.parking_cost}), 200


@user_bp.route('/reservation/current', methods=['GET'])
@user_required
def current_reservation():
    reservation = Reservation.query.filter_by(user_id=current_user.id, leaving_timestamp=None).order_by(Reservation.id.desc()).first()
    if not reservation:
        return jsonify({"error": "No active reservation"}), 404

    spot = ParkingSpot.query.get(reservation.spot_id)
    lot = ParkingLot.query.get(spot.lot_id)

    return jsonify({
        "id": reservation.id,
        "spot_number": f"{spot.id}",
        "lot_name": lot.location_name,
        "booking_time": reservation.booking_timestamp,
        "entry_time": reservation.parking_timestamp,
        "status": "Occupied" if reservation.parking_timestamp else "Reserved"
    }), 200

@user_bp.route('/history', methods=['GET'])
@user_required
def parking_history():
    reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    result = []
    for r in reservations:
        result.append({
            "lot": r.spot.lot.location_name,
            "spot_id": r.spot_id,
            "booking_time": r.booking_timestamp,
            "start": r.parking_timestamp,
            "end": r.leaving_timestamp,
            "cost": r.parking_cost
        })
    return jsonify(result), 200