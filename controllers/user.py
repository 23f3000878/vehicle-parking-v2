from flask import Blueprint, jsonify


user_bp = Blueprint('user',__name__,url_prefix='/user')




# Get Requests
@user_bp.route('/users', methods=['GET'])
def get_users():
    return jsonify({"message": "List of users"})

## Find all available lots(search by location)

## Find recent parking history of the current user

## Find monthly graph reports


# Post Requests

## Book a parking spot

## Finish a parking session