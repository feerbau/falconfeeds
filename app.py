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

class FalconFeeds:

    def __init__(self, data):
        self.event_type = data['eventType']
        self.event_triggered_at = data['eventTriggeredAt']
        self.category = data['data']['category']
        self.threat_actors = data['data']['threatActors']
        self.victims = data['data']['victims']
        self.title = data['data']['title']
        self.content = data['data']['content']
        self.url = data['data']['publishedURL']
    
    def is_threat_feed_event(self):
        return self.event_type == Event.THREAT_FEED.value
    
    def is_ransomware(self):
        return self.category == Category.RANSOMWARE.value
    
    def get_threat_actors(self):
        return [threat_actor['name'] for threat_actor in self.threat_actors]
    
    def list_items_in(self, countries):
        in_list = []
        for country in countries:
            if country in country_victims:
                in_list.append(country)
        return in_list
    
    def country_victim_in(self, country_victims):
        victims = []
        if self.victims is None:
            print("No hay victimas para: " + self.title + " - de cat: " + self.category + " - tipo : " + self.event_type)
        for data in self.victims:
            if data['type'] == 'Country':
                for country in data['values']:
                    if country in country_victims:
                        victims.append(country)
        return victims

    def receive_webhook(self):
        victims = []
        countries = self.country_victim_in(country_victims)
        print("Nuevo incidente de " + self.category + " en " + ', '.join(countries))
        if self.is_threat_feed_event() and self.is_ransomware() and countries != []:
            print("Hola")
            # enviar_incidente(TG_TOKEN_KEY, CHAT_ID, self.title, self.content, self.category, self.url, countries, ', '.join(self.get_threat_actors()))
        else:
            return False
        return True


def verify_basic_auth(username, password):
    return username == Config.BASIC_AUTH_USERNAME and password == Config.BASIC_AUTH_PASSWORD


@app.route('/webhooks/falconfeeds', methods=['POST'])
def falconfeeds_webhook():
    auth = request.authorization
    if not auth or not verify_basic_auth(auth.username, auth.password):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    falcon_feeds = FalconFeeds(data)
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
