from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import Flask, request, jsonify
import os
from database import (
    init_app,
    config_db,
    db
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
from models.post import Post, post_country_association
from utils import (
    enviar_incidente,
    country_victims,
)

load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
app.json.sort_keys = False
init_app(app)
config_db(app)


def verify_basic_auth(username, password):
    return username == Config.BASIC_AUTH_USERNAME and password == Config.BASIC_AUTH_PASSWORD


@app.route('/webhooks/falconfeeds', methods=['POST'])
def falconfeeds_webhook():
    auth = request.authorization
    if not auth or not verify_basic_auth(auth.username, auth.password):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    if 'uuid' in data['data']:
        post = Post.query.filter_by(uuid=data['data']['uuid']).first()
        if post is not None:
            return jsonify(message="Duplicated"), 200
    falcon_feeds = FalconFeedsService(data)
    ok = falcon_feeds.receive_webhook()
    if ok:
        return jsonify(message="Webhook received"), 200
    return jsonify(message="Fail!"), 400


@app.route('/stats/threat_actors', methods=['GET'])
def get_stats_by_threat_actor():
    date = request.args.get('date')
    name = request.args.get('name')
    stats = {}
    query = ThreatActor.query

    if date:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        date.replace(day=1)
        query = query.join(ThreatActor.posts).filter(Post.published_at.between(date, date + relativedelta(months=1)))
    if name:
        query = query.filter(ThreatActor.name == name)

    for threat_actor in query.all():
        stats[threat_actor.name] = threat_actor.posts.count()
    stats = {k: v for k, v in sorted(stats.items(), key=lambda item: item[1], reverse=True)}
    return stats


@app.route('/stats/countries', methods=['GET'])
def get_stats_by_country():
    date = request.args.get('date')
    name = request.args.get('name')
    stats = {}
    query = (
        db.session.query(Post, Country)
        .select_from(Post)
        .join(post_country_association, Post.id == post_country_association.c.post_id)
        .join(Country, post_country_association.c.country_id == Country.id)
    )

    if date:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        date.replace(day=1)
        query = query.filter(Post.published_at.between(date, date + relativedelta(months=1)))
    if name:
        query = query.filter(Country.name == name)

    for country in query.all():
        stats[country.name] = country.posts.count()
    return stats

if __name__ == "__main__":
    app.run(host=Config.APP_RUN_HOST, port=Config.PORT, debug=Config.DEBUG)
