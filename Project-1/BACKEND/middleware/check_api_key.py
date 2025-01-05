from flask import jsonify, request
# from helpers import logger

# Middleware to check API Key and session validity
def check_api_key(request):
    # Validate API Key
    api_key = request.headers.get("X-API-KEY")
    valid_api_key = "axsdTypoiUYTfsv89**hqiu19&&&" # Replace with your actual API key

    if not api_key or api_key != valid_api_key:
        # logger.error("Invalid API Key.")
        return jsonify({"error": "Unauthorized", "message": "Invalid API Key"}), 401
    
    return None # No Errors, continue to the endpoint.
