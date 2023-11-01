from flask import Flask, request, Response
from functions import *
import json

app = Flask(__name__)

MAX_ID_LEN = 6

@app.route('/api/v1/drivers', methods = ['POST'])
def add_driver():
    form_data = request.json
    json_str = json.dumps(form_data, indent=4, sort_keys=True)
    print(json_str)

    if form_data["profile"]["email"] == "":
        return Response("email_id absent", status=400, mimetype='application/json')


    # check if email already exists in the db. If yes, return error, else add the entry
    data = fetch_driver_row(form_data["profile"]["email"])
    if data:
        if hashlib.sha512(form_data["credentials"]["password"]["value"].encode('UTF-8')).hexdigest() == data[0][3]:
            return Response("driver data already exists", status=400, mimetype='application/json')
        else:
            return Response("unauthorized access", status=500, mimetype='application/json')
        
    else:
        row_data = {
            "email_id": form_data["profile"]["email"],
            "first_name": form_data["profile"]["first_name"],
            "last_name": form_data["profile"]["last_name"],
            "mobile": form_data["profile"]["mobile"],

            "pwd": form_data["credentials"]["password"]["value"],

            "plate_number": form_data["vehicle_details"]["plate_number"],
            "vehicle": form_data["vehicle_details"]["vehicle"],

            "is_available": False,
            "onb_status": "Not Started",
            "onb_comment": ""
        }
        insert_driver_row(row_data)
        return row_data

@app.route('/api/v1/drivers/<string:email_id>/onboard', methods = ['POST']) # ?email_id=umangnangal@gmail.com
def trigger_onboarding_process(email_id: str):
    if email_id == "":
        print("user email_id not provided!")
        return

    row_data = {
        "email_id": email_id,
        "status": "Awaiting Action",
        "comment": "",
        "action_by": ""
    }
    insert_approval_row(row_data)
    return row_data

@app.route('/api/v1/approvals', methods = ['GET'])
def get_approvals():
    data = list_all_approvals()
    resp_data = {
        "data": data
    }
    return resp_data

@app.route('/api/v1/approvals/<string:email_id>', methods = ['POST'])
def approval_action_by_admin(email_id: str):

    if email_id == "":
        print("user email_id not provided!")
        return
    
    form_data = request.json
    json_str = json.dumps(form_data, indent=4, sort_keys=True)
    print(json_str)

    action = form_data["action"]
    comment = form_data["comment"]

    if action not in ["Accept", "Decline"]:
        print("invalid action!")
        return

    row_data = {
        "email_id": email_id,
        "status": action,
        "comment": comment,
        "action_by": "admin"
    }
    update_approval_row(row_data)

    # update onb_status and comment in driver table
    update_driver_row(row_data)

    return row_data

@app.route('/api/v1/drivers', methods = ['GET'])
def get_drivers():
    data = fetch_drivers()
    resp_data = {
        "data": data,
    }
    return resp_data

@app.route('/api/v1/drivers/<string:email_id>', methods = ['GET'])
def get_driver_info(email_id):
    data = fetch_driver_info(email_id)
    resp_data = {
        "data": data[0] if len(data) else [],
    }
    return resp_data

@app.route('/api/v1/drivers/<string:email_id>/availability', methods = ['GET'])
def is_driver_available(email_id: str) -> bool:
    data = fetch_driver_row(email_id)
    resp_data = {
        "isAvailable": True if data[7] else False
    }

    return resp_data

@app.route('/api/v1/drivers/<string:email_id>/availability', methods = ['POST'])
def toggle_driver_availability(email_id: str):
    data = fetch_driver_row(email_id)
    row_data = {
        "email_id": email_id,
        "is_available": data[7]^1
    }
    update_driver_availability(row_data)
    return row_data


if __name__ == '__main__':
    init_tables()
    app.run(host="0.0.0.0", port=5001)
