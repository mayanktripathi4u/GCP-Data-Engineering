from flask import jsonify
from helpers.options_helper import add_options_headers

def get_info(request):
    auth_header = request.headers.get('X-AP_kYE')

    if not auth_header:
        return jsonify({"error": "Unauthorized"}), 401
    
    response_data = {
        "message" : "success"
    }

    response = jsonify(response_data)
    response.status_code = 200

    return add_options_headers(response=response)

