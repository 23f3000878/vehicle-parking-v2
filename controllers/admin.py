from flask import Blueprint, jsonify


admin_bp = Blueprint('admin',__name__,url_prefix='/admin')



# Get Requests
@admin_bp.route('/', methods=['GET'])
def get_admin():
    return jsonify({"message": "List of admins"})

## Get All Lots

## Get All Spots by lot id

## Get occupied parking spot details

## Get Lots Info Graph

## Get Spots Info Graph


# Post Requests

## Create a new lot( also creates spots for this lot automatically)

## Update lot information (add or delete available spots, according to the updated, number of spots)()



# Delete Requests

## Delete a lot ( also delete all its spot )

## Delete a spot ( can delete only if, it is not occupied) 

# Update Requests

## Update lot information

## Update number of spots in a lot

## Update spot information 