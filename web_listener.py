from flask import Flask, request, redirect, url_for
import logging

app = Flask(__name__)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='auth_listener.log'
)
logger = logging.getLogger(__name__)

@app.route('/auth/consent')
def auth_consent():
    code = request.args.get('code')
    if code:
        logger.info(f"Authorization code received: {code}")
        # Here you can exchange the authorization code for an access token
        # For example, you might call a function like exchange_code_for_token(code)
        return "Authorization code received. You can close this window."
    else:
        logger.error("No authorization code found in the request.")
        return "Consent successful. You can close this window."

@app.route('/auth/callback')
def auth_callback():
    code = request.args.get('code')
    if code:
        logger.info(f"Authorization code received: {code}")
        # Here you can exchange the authorization code for an access token
        # For example, you might call a function like exchange_code_for_token(code)
        return "Authorization code received. You can close this window."
    else:
        logger.error("No authorization code found in the request.")
        return "Error: No authorization code found in the request."

if __name__ == '__main__':
    app.run(port=5000)