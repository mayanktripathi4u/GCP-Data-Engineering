from flask import Flask, request, jsonify
from helpers.options_helper import process_options_response
from middleware import check_api_key
from endpoints import get_info

app = Flask(__name__)

@app.before_request
def check_authentication():
    # Handle options request - An OPTIONS request is a method in HTTP that allows a client to determine the communication options for a specific resource or server.
    if request.method == 'OPTIONS':
        return process_options_response()
    
    # Check if the request path if for the AI update endpoint. For timebeing I am using same logic ot check_api_key() just to showcase that we have multiple middleware being called.
    if request.path in ['/v1/getInfo']:
        # Call the check_api_key middleware
        auth_fail_response = check_api_key(request) # CHange the logic based on requirement 
    else:
        # Use other authentication checks
        auth_fail_response = check_api_key(request) # CHange the logic based on requirement

    if auth_fail_response:
        print(f"AUTH FAIL {auth_fail_response}")
        return auth_fail_response
    else:
        print("AUTH SUCCESS")

# Endpoint to get Information
@app.route('/v1/getInfo', methods = ['POST', 'OPTIONS'])
def getInfo():
    return get_info(request) # Call the new update entity function

# Endpoint for root
@app.route('/')
def hello_world():
    return """Hello Worlds! Thanks for pingings us!
    
    You have reached the AI Langiage root API. Go to www.theailanguage.com to start building."""

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=8080, debug=True)