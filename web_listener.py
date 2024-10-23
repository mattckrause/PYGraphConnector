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

@app.route('/auth/callback')
def auth_callback():
    logger.info("Admin consent was received.")
    tenant = request.args.get('tenant')

    if request.args.get('admin_consent') == 'true':
        return "Admin consent was received. You can close this window."
    else:
        return "Error: Admin consent was not received. Please try again."


if __name__ == '__main__':
    app.run(port=5000)