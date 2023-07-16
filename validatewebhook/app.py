from flask import Flask, request, jsonify
import hashlib
import hmac
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

YOUR_WEBHOOK_SECRET = os.getenv("YOUR_WEBHOOK_SECRET")

@app.route('/zoom-webhook', methods=['POST'])
def validate_webhook():
    # Parse the incoming JSON request
    data = request.get_json()

    # Log the incoming webhook data
    app.logger.info(f"Received data: {data}")

    # Ensure the request is a CRC validation
    if data['event'] != 'endpoint.url_validation':
        return 'Unexpected event type', 400

    # Get the plain token from the request
    plain_token = data['payload']['plainToken']

    # Create the HMAC SHA-256 hash
    hash_obj = hmac.new(YOUR_WEBHOOK_SECRET.encode('utf-8'), 
                        plain_token.encode('utf-8'), 
                        hashlib.sha256)
    encrypted_token = hash_obj.hexdigest()

    # Create the response JSON object
    response = {
        'plainToken': plain_token,
        'encryptedToken': encrypted_token
    }

    # Respond within 3 seconds with a 200 or 204 HTTP response code.
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=8000)
