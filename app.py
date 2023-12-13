from flask import Flask, request, jsonify
import os
from database import (
    init_app,
    config_db
)
from config import Config
from services.falconfeeds import FalconFeedsService
from dotenv import load_dotenv
from models.threat_actor import ThreatActor
from models.site import Site
from models.industry import Industry
from models.country import Country
from models.organization import Organization
from models.image import Image
from models.post import Post

load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
init_app(app)
config_db(app)


@app.route('/webhooks/falconfeeds', methods=['POST'])
def falconfeeds_webhook():
    #TODO: Autorizacion
    data = request.get_json()
    falcon_feeds = FalconFeedsService(data)
    ok = falcon_feeds.receive_webhook()
    if ok:
        return jsonify(message="Webhook received"), 200
    return jsonify(message="Fail!"), 400
    

if __name__ == "__main__":
    app.run(port=Config.PORT, debug=Config.DEBUG)

    