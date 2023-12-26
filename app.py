from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
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


basic_auth = BasicAuth(app)

@app.route('/webhooks/falconfeeds', methods=['POST'])
@basic_auth.required
def falconfeeds_webhook():
    #TODO: Autorizacion
    data = request.get_json()
    if 'uuid' in data['data']:
        post = Post.query.filter_by(uuid=data['data']['uuid']).first()
        if post is not None:
            return jsonify(message="Duplicated"), 200
    falcon_feeds = FalconFeedsService(data)
    ok = falcon_feeds.receive_webhook()
    if ok:
        return jsonify(message="Webhook received"), 200
    return jsonify(message="Fail!"), 200

if __name__ == "__main__":
    app.run(port=Config.PORT, debug=Config.DEBUG)

    