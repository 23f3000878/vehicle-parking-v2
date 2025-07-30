from flask import Blueprint, jsonify, Flask, abort, request, g
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from datetime import datetime, timedelta, timezone
from model import db,User, Lot, Spot, ReserveSpot
from extensions import cache
from decorators import login_required
from .user_cache import delete_user_cache

admin_bp = Blueprint('admin',__name__,url_prefix='/admin')


#Pre Creating Admin
def create_admin():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(email='admin@parkus.com',role='admin',fullname='Admin',)
        admin.set_password('admin')  # Set a secure password
        db.session.add(admin)
        db.session.commit()

# Admin required decorator
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()
        if current_user.role!='admin':  # Check if the current user is an admin
            abort(403,{"error":"This route is protected only for admin!"})  # Forbidden access
        return f(*args, **kwargs)
    return decorated_function


# --------------------------------------------------Get Requests-------------------------------------------------

## Get Filtered Lots

### Memoized Helper Function
cache.memoize(timeout=300)
def get_filtered_lots(location, name, created_at_lower, no_of_spots_upper):
    query = Lot.query

    if location:
        query = query.filter(Lot.prime_location_name.ilike(f"%{location}%"))
    if name:
        query = query.filter(Lot.name.ilike(f"%{name}%"))
    if created_at_lower:
        try:
            date_obj = datetime.strptime(created_at_lower, "%Y-%m-%d")
            query = query.filter(Lot.created_at >= date_obj)
        except ValueError:
            return {'error':'ValueError'}, 500
    if no_of_spots_upper is not None:
        query = query.filter(Lot.no_of_spots <= no_of_spots_upper)

    lots = query.all()
    return [{
        "id": lot.id,
        "name": lot.name,
        "location": lot.prime_location_name,
        "price": lot.price,
        "address": lot.address,
        "pincode": lot.pincode,
        "no_of_spots": lot.no_of_spots,
        "created_at": lot.created_at.strftime("%Y-%m-%d %H:%M:%S")
    } for lot in lots], 200

### Route
@admin_bp.route('/lots/filter', methods=['GET'])
@admin_required
def search_lots():
    location = request.args.get('location')
    name = request.args.get('name')
    created_at_lower = request.args.get('created_at_lower')
    no_of_spots_upper = request.args.get('no_of_spots_upper', type=int)

    data, status = get_filtered_lots(location, name, created_at_lower, no_of_spots_upper)
    if data is None:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    return jsonify(data), status



## Get Filtered Registerd Users

### Cache Helper Function
@cache.memoize(timeout=300)
def find_all_users(name,address):
    query = User.query
    if name:
        query = query.filter(User.fullname.ilike(f'%{name}%'))
    
    if address:
        query = query.filter(User.address.ilike(f'%{address}%'))

    users = query.filter_by(role='user').all()
    user_list = []
    for user in users:
        user_info = {
            "id": user.id,
            "email": user.email,
            "fullname": user.fullname,
            "address":user.address
        }
        user_list.append(user_info)
    
    return user_list

### Route
@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    name = request.args.get("name")
    address = request.args.get("address")

    user_list = find_all_users(name,address)
    
    return jsonify({"users": user_list}), 200


## -----------------Spots Endpoints-------------------------------------

## Get All Spots by lot id

### Cache Helper Function
@cache.memoize(timeout=300)
def find_spots_by_lot(lot_id):
    lot = Lot.query.get(lot_id)
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

### Route
@admin_bp.route('/lots/<int:lot_id>/spots', methods=['GET'])
@admin_required
def get_spots_by_lot(lot_id):
    spot_list = find_spots_by_lot(lot_id)
    return jsonify({"spots": spot_list}), 200

## Get general parking spot details
### Cache Helper Function
@cache.memoize(timeout=300)
def find_all_spots(spot_id):
    spot = Spot.query.get(spot_id)
    if not spot:
        return {"message": "Spot not found"}, 404
    
    spot_info = {
        "id": spot.id,
        "spot_number": spot.spot_number,
        "status": spot.status
    }
    return {"spot": spot_info}, 200

@admin_bp.route('/spots/<int:spot_id>', methods=['GET'])
@admin_required
def get_all_spots(spot_id):
    data,status = find_all_spots(spot_id)
    return jsonify(data), status


## Get occupied parking spot details

### Helper Function
@cache.memoize(timeout=300)
def find_occupied_spots(spot_id):
    spot = Spot.query.get(spot_id)
    if not spot or spot.status != 'O':
        return {"message": "Spot not found or not occupied"}, 404
    
    reserve_spot = ReserveSpot.query.filter_by(spot_id=spot_id).first()
    if not reserve_spot:
        return {"message": "No reservation found for this spot"}, 404
    
    spot_info = {
        "id": spot.id,
        "customer_id": reserve_spot.user_id,
        "vehicle_no": reserve_spot.vehicle_no,
        "reserved_by": reserve_spot.user.email,
        "estimated_cost": reserve_spot.cost,
        "parking_time": reserve_spot.parking_time,
    }
    return {'spot':spot_info}, 200

### Route
@admin_bp.route('/spots/<int:spot_id>/occupied', methods=['GET'])
@admin_required
def get_occupied_spots(spot_id):
    data,status = find_occupied_spots(spot_id)
    return jsonify(data), status


# -----------------------Graph Data Endpoints------------------------------------

## Get Overall Occupancy Trend(% of occupied spots per day, for previous 7 days)
@admin_bp.route('/spots/occupancy-trend', methods=['GET'])
@admin_required
@cache.cached(timeout=300,key_prefix=lambda: f'occupancy-graph-{g.current_user.id}')
def get_occupancy_trend():
    today = datetime.now(timezone.utc)
    occupancy_trend = []

    for i in range(7):
        date = today - timedelta(days=i)
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)

        total_spots = Spot.query.filter(Spot.created_at >= start_of_day, Spot.created_at <= end_of_day).count()
        occupied_spots = Spot.query.filter(Spot.status == 'O', Spot.created_at >= start_of_day, Spot.created_at <= end_of_day).count()

        occupancy_percentage = (occupied_spots / total_spots * 100) if total_spots > 0 else 0
        occupancy_trend.append({
            "date": date.strftime('%Y-%m-%d'),
            "occupancy_pct": occupancy_percentage
        })
    occupancy_trend.reverse()

    return jsonify({"occupancy_trend": occupancy_trend}), 200

## Get Lot By Lot Availability Graph(Available vs Occupied Spots)
@admin_bp.route('/lots/availability', methods=['GET'])
@admin_required
@cache.cached(timeout=300,key_prefix=lambda:f'availability-graph-{g.current_user.id}')
def get_lot_availability():
    lots = Lot.query.all()
    availability_data = []

    for lot in lots:
        total_spots = Spot.query.filter_by(lot_id=lot.id).count()
        occupied_spots = Spot.query.filter_by(lot_id=lot.id, status='O').count()
        available_spots = total_spots - occupied_spots

        lot_info = {
            "lot_id": lot.id,
            "name": lot.name,
            "available_spots": available_spots,
            "occupied_spots": occupied_spots
        }
        availability_data.append(lot_info)

    return jsonify({"availability": availability_data}), 200


## Get Revenue Per Parking Lot Graph
@admin_bp.route('/lots/revenue', methods=['GET'])
@admin_required
@cache.cached(timeout=300,key_prefix=lambda: f'lots-revenue-graph-{g.current_user.id}')
def get_lot_revenue():  
    lots = Lot.query.all()
    revenue_data = []

    for lot in lots:
        total_revenue = db.session.query(db.func.sum(ReserveSpot.cost*((db.func.julianday(ReserveSpot.leaving_time) - db.func.julianday(ReserveSpot.parking_time))*24))).filter(ReserveSpot.spot.has(lot_id=lot.id), ReserveSpot.leaving_time.isnot(None)).scalar() or 0

        lot_info = {
            "lot_id": lot.id,
            "name": lot.name,
            "total_revenue": total_revenue
        }
        revenue_data.append(lot_info)

    return jsonify({"revenue": revenue_data}), 200

## Get Top Users by Revenue Graph
@admin_bp.route('/users/top-revenue', methods=['GET'])
@admin_required
@cache.cached(timeout=300,key_prefix=lambda: f'top-revenue-graph-{g.current_user.id}')
def get_top_users_by_revenue():
    # Logic to retrieve top users by revenue
    top_users = db.session.query(User, db.func.sum(ReserveSpot.cost).label('total_revenue')) \
        .join(ReserveSpot, User.id == ReserveSpot.user_id) \
        .group_by(User.id) \
        .order_by(db.desc('total_revenue')) \
        .limit(10) \
        .all()

    user_revenue_data = []
    for user, total_revenue in top_users:
        user_info = {
            "user_id": user.id,
            "email": user.email,
            "total_revenue": total_revenue
        }
        user_revenue_data.append(user_info)

    return jsonify({"top_users": user_revenue_data}), 200




# -----------------------------------------------Post Requests----------------------------------------------------------

## Create a new lot( also creates spots for this lot automatically)
@admin_bp.route('/lots', methods=['POST'])
@admin_required
def create_new_lot():
    # Logic to create a new lot
    try:
        data = request.get_json()
        if not data or 'prime_location_name' not in data or 'price' not in data or 'address' not in data or 'pincode' not in data or 'no_of_spots' not in data:
            return jsonify({"message": "Invalid input"}), 400
        name = data.get('name', 'New Lot')  # Default name if not provided

        new_lot = Lot(name=data['name'], prime_location_name=data['prime_location_name'], price=data['price'], address=data['address'], pincode=data['pincode'], no_of_spots=data['no_of_spots'])
        db.session.add(new_lot)
        db.session.commit()
        
        # Create spots for the new lot
        for i in range(new_lot.no_of_spots):

            new_spot = Spot(lot_id=new_lot.id, spot_number=i+1, status='A')
            db.session.add(new_spot)
        
        db.session.commit()

        # Delete lots and spots cache
        cache.delete(f'availability-graph-{g.current_user.id}')
        cache.delete(f'occupancy-graph-{g.current_user.id}')
        cache.delete(f'lots-revenue-graph-{g.current_user.id}')
        cache.delete_memoized(get_filtered_lots)
        cache.delete_memoized(find_spots_by_lot)
        delete_user_cache()
        
        return jsonify({"message": "Lot created successfully", "lot_id": new_lot.id}), 201
    except:
        return jsonify({"error":"Unique constraint failed or Invalid Input."})

# -------------------------------------------------Delete Requests------------------------------------------------------

## Delete a lot ( also delete all its spot )
@admin_bp.route('/lots/<int:lot_id>', methods=['DELETE'])
@admin_required
def delete_lot(lot_id):
    # Logic to delete a lot
    lot = Lot.query.get(lot_id)
    if not lot:
        return jsonify({"message": "Lot not found"}), 404
    
    db.session.delete(lot)
    db.session.commit()

    # Delete lots and spots cache
    cache.delete(f'availability-graph-{g.current_user.id}')
    cache.delete(f'occupancy-graph-{g.current_user.id}')
    cache.delete(f'lots-revenue-graph-{g.current_user.id}')
    cache.delete_memoized(get_filtered_lots)
    cache.delete_memoized(find_spots_by_lot)
    delete_user_cache()
    
    return jsonify({"message": "Lot deleted successfully"}), 200

## Delete a spot ( can delete only if, it is not occupied) 
@admin_bp.route('/spot/<int:spot_id>',methods=['DELETE'])
@admin_required
def delete_spot(spot_id):
    spot = Spot.query.get(spot_id)
    if not spot:
        return jsonify({"message":"No spot found!"})
    if spot.status != 'A':
        return jsonify({"message":"This spot is Occupied!"})
    db.session.delete(spot)
    db.session.commit()

    # Delete Spots Cache
    cache.delete(f'occupancy-graph-{g.current_user.id}')

    return jsonify({"message": "Spot deleted successfully"}), 200

# -------------------------------------------------Update Requests-----------------------------------------------------

## Update lot information
@admin_bp.route('/lots/<int:lot_id>', methods=['PUT'])
@admin_required
def update_new_lot(lot_id):
    # Logic to update a lot
    data = request.get_json()
    lot = Lot.query.filter_by(id=lot_id).first()
    if not data:
        return jsonify({"message": "Invalid input"}), 400
    # print(data["name"],type(data))
    if 'name' in data.keys():
        lot.name = data["name"]
    if 'prime_location_name' in data.keys():
        lot.prime_location_name = data["prime_location_name"]
    if 'price' in data.keys():
        lot.price = data["price"]
    if 'address' in data.keys():
        lot.address = data["address"]
    if 'pincode' in data.keys():
        lot.pincode = data["pincode"]
    if 'no_of_spots' in data.keys():
        no_of_spots = data["no_of_spots"]    
        # Update spots based on the new number of spots
        if no_of_spots > lot.no_of_spots:
            # If the new number of spots is greater, add new spots
            for i in range(lot.no_of_spots, no_of_spots):
                new_spot = Spot(lot_id=lot.id, spot_number=i+1, status='A')
                db.session.add(new_spot)
        elif no_of_spots < lot.no_of_spots and no_of_spots > 0:
            # If the new number of spots is less, delete excess spots
            excess_spots = Spot.query.filter_by(lot_id=lot.id).order_by(Spot.spot_number.desc()).limit(lot.no_of_spots - no_of_spots).all()
            for spot in excess_spots:
                db.session.delete(spot)

        lot.no_of_spots = no_of_spots
    db.session.add(lot)
    db.session.commit()

    # Delete lots and spots cache
    cache.delete(f'availability-graph-{g.current_user.id}')
    cache.delete(f'occupancy-graph-{g.current_user.id}')
    cache.delete(f'lots-revenue-graph-{g.current_user.id}')
    cache.delete_memoized(get_filtered_lots)
    cache.delete_memoized(find_spots_by_lot)
    cache.delete_memoized(find_all_spots)
    cache.delete_memoized(find_occupied_spots)
    delete_user_cache()
    
    return jsonify({"message": "Lot updated successfully"}), 201
