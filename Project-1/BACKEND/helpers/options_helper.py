from flask import jsonify

def process_options_response():
    # COrrected CORS preflight response
    response = jsonify({}) # Empty Response
    response.status_code = 204
    return add_options_headers(response)

def add_options_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Authorization, Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    return response

