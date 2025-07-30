from model import Lot,db, ReserveSpot, Spot, User
from flask import Blueprint, jsonify, g, request
from datetime import datetime, timezone, timedelta
from extensions import cache
from decorators import login_required
from tasks import export_bookings_to_csv
from .admin_cache import delete_lots_cache,delete_spots_cache


user_bp = Blueprint('user',__name__,url_prefix='/user')


# --------------------------Get Requests-----------------------------------------------

## Find about me
@user_bp.route('/me', methods=['GET'])
@login_required
@cache.cached(timeout=300,key_prefix=lambda: f"me:{g.current_user.id}")
def get_users():
    user = g.current_user
    return jsonify({'email':user.email,'id':user.id,'fullname':user.fullname,'address':user.address,'role':user.role})



## Find all available lots(search by location)

### Helper Function
@cache.memoize(timeout=300)
def find_lots(location):
    query = Lot.query
    if location:
        query = query.filter(Lot.prime_location_name.ilike(f"%{location}%"))
    lots = query.order_by(Lot.created_at.desc()).all()
    lots_data = []
    for lot in lots:
        occupied_count = sum(1 for s in lot.spots if s.status == 'O')
        if lot.no_of_spots == occupied_count:
            continue
        entry = {
                'id': lot.id,
                'name': lot.name,
                'location': lot.prime_location_name,
                'created_at': lot.created_at.isoformat(),
                'price': lot.price,
                'address':lot.address,
                'pincode':lot.pincode,
                'total_spots':lot.no_of_spots,
                'available_spots': lot.no_of_spots - occupied_count, 
                
            }
        lots_data.append(entry)
    return lots_data

### Route
@user_bp.route('/lots', methods=['GET'])
@login_required
def get_available_lots():
    location = request.args.get('location')
    
    lots_data = find_lots(location)
    return jsonify(lots_data)



## Get All Spots by lot id
### Cache Helper Function
@cache.memoize(timeout=300)
def find_all_spots(lot_id):
    spots = Spot.query.filter_by(lot_id=lot_id).all()
    spot_list = []
    for spot in spots:
        spot_info = {
            "id": spot.id,
            "spot_number": spot.spot_number,
            "status": spot.status
        }
        spot_list.append(spot_info)
    
    return spot_list

@user_bp.route('/lots/<int:lot_id>/spots', methods=['GET'])
@login_required
def get_spots_by_lot(lot_id):
    spot_list = find_all_spots(lot_id)
    return jsonify({"spots": spot_list}), 200




## Find recent parking history of the current user
@user_bp.route('/reservations',methods=['GET'])
@login_required
@cache.cached(timeout=300, key_prefix=lambda: f"parking-history:{g.current_user.id}")
def get_history():
    reservations = ReserveSpot.query.filter_by(user_id=g.current_user.id).all()

    if not reservations:
        return jsonify({'error':'Nothing found'})
    
    reservation_list = []

    for reservation in reservations:
        entry = {
            "id":reservation.id,
            "vehicle_no":reservation.vehicle_no,
            "parking_time":reservation.parking_time.isoformat(),
            "leaving_time":reservation.leaving_time and reservation.leaving_time.isoformat(),
            "location":reservation.location,
            "price":reservation.spot.lot.price,
            "total_cost":reservation.cost,
            "status":"released" if reservation.leaving_time else "parked"
        }
        reservation_list.append(entry)

    return jsonify(reservation_list)



## -----------------------Graph reports--------------------

## Find Status Summary(Pie Chart) of any Lot

### Cache Helper Function
cache.memoize(timeout=300)
def find_lot_status(lot_id):
    lot = Lot.query.get_or_404(lot_id)
    total = len(lot.spots)
    
    available = len([s for s in lot.spots if s.status == 'A'])
    occupied = total - available
    return (available, occupied)

### Route
@user_bp.route('/status-summary/<int:lot_id>',methods=['GET'])
@login_required
# @cache.cached(timeout=300,key_prefix=lambda: f"status-summary-{g.current_user.id}")
def lot_status_summary(lot_id):
    available,occupied = find_lot_status(lot_id)

    return jsonify({
        'available': available,
        'occupied': occupied
    })


## Find Booking History(Bar Chart) of current user(previous week)
@user_bp.route('/my-booking-history', methods=['GET'])
@login_required
@cache.cached(timeout=300, key_prefix=lambda: f"booking-history:{g.current_user.id}")
def booking_history():
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    seven_days_ago = today - timedelta(days=6)

    # Get booking count per day
    history = db.session.query(
        db.func.date(ReserveSpot.parking_time).label('day'),
        db.func.count().label('count')
    ).filter(
        ReserveSpot.user_id == g.current_user.id,
        ReserveSpot.parking_time >= seven_days_ago
    ).group_by(db.func.date(ReserveSpot.parking_time)).all()

    # Convert query result to a dictionary {date: count}
    count_map = { day: count for day, count in history }

    # Build the final list with all 7 days
    full_data = []
    for i in range(7):
        day = (today - timedelta(days=i)).date()
        formatted_day = day.strftime('%Y-%m-%d')
        full_data.append({
            "date": formatted_day,
            "count": count_map.get(str(day), 0)
        })

    full_data.reverse()  # Optional: Chronological order (oldest to newest)

    return jsonify(full_data)

# ------------------------Post Requests-----------------------------------------------

## Book a parking spot
@user_bp.route('/book', methods=['POST'])
@login_required
def book_parking_spot():
    data = request.get_json()
    lot_id = data.get('lot_id')
    spot_id = data.get('spot_id')
    vehicle_no = data.get('vehicle_no')
    parking_time  = datetime.fromisoformat(data.get('parking_time').replace("Z", "+00:00"))

    if not lot_id or not spot_id:
        return jsonify({'error': 'lot_id and spot_id are required'}), 400

    lot = Lot.query.get(lot_id)
    if not lot:
        return jsonify({'error': 'Lot not found'}), 404

    spot = next((s for s in lot.spots if s.id == spot_id), None)
    if not spot:
        return jsonify({'error': 'Spot not found'}), 404

    if spot.status == 'O':
        return jsonify({'error': 'Spot already occupied'}), 400

    # Mark the spot as occupied and assign to user
    spot.status = 'O'

    reservation= ReserveSpot(spot_id=spot.id,user_id=g.current_user.id, vehicle_no=vehicle_no,location=lot.prime_location_name,cost=lot.price,parking_time=parking_time)
    
    db.session.add(reservation)
    db.session.commit()

    # Delete cache of lots and spots
    cache.delete(f"booking-history:{g.current_user.id}")
    cache.delete(f"parking-history:{g.current_user.id}")
    cache.delete_memoized(find_lots)
    cache.delete_memoized(find_lot_status)
    cache.delete_memoized(get_spots_by_lot)
    cache.delete_memoized(find_all_spots)
    delete_lots_cache()
    delete_spots_cache()

    return jsonify({'message': 'Spot booked successfully','id':reservation.id, 'spot_id': spot.id, 'lot_id': lot.id,'location':lot.prime_location_name})



# ----------------------Put Requests -------------------------------------------

## Edit profile information
@user_bp.route('/profile/edit',methods=['PUT'])
@login_required
def edit_profile():
    data = request.get_json()
    user = User.query.get(g.current_user.id)

    if 'fullname' in data:
        user.fullname = data['fullname']
    
    if 'address' in data:
        user.address = data['address']
    
    db.session.commit()

    # Delete cache of lots and spots
    cache.delete(f"me:{g.current_user.id}")

    return jsonify({'msg':'User Updated Successfully.'})


## Release a parking session
@user_bp.route('/finish', methods=['PUT'])
@login_required
def finish_parking_session():
    data = request.get_json()
    reservation_id = data.get('reservation_id')
    releasing_time = datetime.fromisoformat(data.get('releasing_time').replace("Z", "+00:00"))
    cost = data.get('cost')

    if not reservation_id:
        return jsonify({'error': 'reservation_id is required'}), 400

    reservation = ReserveSpot.query.get(reservation_id)
    if not reservation:
        return jsonify({'error': 'Reservation not found'}), 404

    if reservation.user_id != g.current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    spot = Spot.query.get(reservation.spot_id)
    if not spot:
        return jsonify({'error': 'Spot not found'}), 404

    if spot.status != 'O':
        return jsonify({'error': 'Spot is not currently occupied'}), 400

    spot.status = 'A'  # Mark as available
    reservation.leaving_time = releasing_time
    reservation.cost = cost
    db.session.commit()

    # Delete cache of lots and spots
    cache.delete(f"booking-history:{g.current_user.id}")
    cache.delete(f"parking-history:{g.current_user.id}")
    cache.delete_memoized(find_lots)
    cache.delete_memoized(get_spots_by_lot)
    cache.delete_memoized(find_lot_status)
    cache.delete_memoized(find_all_spots)
    delete_lots_cache()
    delete_spots_cache()

    return jsonify({'message': 'Parking session finished and spot is now available', 'spot_id': spot.id})



# ------------------------------------Backend Asynchronous Jobs---------------------------------

@user_bp.route('/export-bookings', methods=['POST'])
@login_required
def export_bookings():
    user_id = g.current_user.id
    task = export_bookings_to_csv.delay(user_id)
    return jsonify({"msg": "Export started", "task_id": task.id})