from enum import Enum
import telebot
from emoji import emojize
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))
TG_TOKEN_KEY = os.environ.get("TG_TOKEN_KEY")
CHAT_ID = os.environ.get("TG_CHAT_ID")
USERNAME = os.environ.get("AUTH_USERNAME")
PASSWORD = os.environ.get("AUTH_PASSWORD")

member_countries_emojis = {
    'Antigua and Barbuda': emojize(":antigua_barbuda:", language='alias')+" (AG)",
    'Bahamas': emojize(":bahamas:", language='alias')+ " (BS)",
    'Barbados': emojize(":barbados:", language='alias')+" (BB)",
    'Belize': emojize(":belize:", language='alias')+ " (BZ)",
    'Canada': emojize(":canada:", language='alias')+ " (CA)", 
    'Dominica': emojize(":dominica:", language='alias')+ " (DM)",
    'Dominican Republic': emojize(":dominican_republic:", language='alias')+ " (DO)",
    'Grenada': emojize(":grenada:", language='alias')+ " (GD)",
    'Guyana': emojize(":guyana:", language='alias')+ " (GY)",
    'Jamaica': emojize(":jamaica:", language='alias')+ " (JM)",
    'Saint Kitts and Nevis': emojize(":st_kitts_nevis:", language='alias')+ " (KN)",
    'Saint Lucia': emojize(":st_lucia:", language='alias')+ " (LC)",
    'Saint Vincent and the Grenadines': emojize(":st_vincent_grenadines:", language='alias')+ " (VC)",
    'Suriname': emojize(":suriname:", language='alias')+ " (SR)",
    'Trinidad and Tobago': emojize(":trinidad_tobago:", language='alias')+ " (TT)",
    'USA': emojize(":us:", language='alias')+ " (US)",
    "Argentina": emojize(":argentina:", language='alias')+ " (AR)",
    "Bolivia": emojize(":bolivia:", language='alias')+ " (BO)",
    "Brazil": emojize(":brazil:", language='alias')+ " (BR)",
    "Chile": emojize(":chile:", language='alias')+ " (CL)",
    "Colombia": emojize(":colombia:", language='alias')+ " (CO)",
    "Costa Rica": emojize(":costa_rica:", language='alias')+ " (CR)",
    "Cuba": emojize(":cuba:", language='alias')+ " (CU)",
    "Ecuador": emojize(":ecuador:", language='alias')+ " (EC)",
    "El Salvador": emojize(":el_salvador:", language='alias')+ " (SV)",
    "Guatemala": emojize(":guatemala:", language='alias')+ " (GT)",
    "Haiti": emojize(":haiti:", language='alias')+ " (HT)",
    "Honduras": emojize(":honduras:", language='alias')+ " (HN)",
    "Mexico": emojize(":mexico:", language='alias')+ " (MX)",
    "Panama": emojize(":panama:", language='alias')+ " (PA)",
    "Paraguay": emojize(":paraguay:", language='alias')+ " (PY)",
    "Peru": emojize(":peru:", language='alias')+ " (PE)",
    "Uruguay": emojize(":uruguay:", language='alias')+ " (UY)",
    "Venezuela": emojize(":venezuela:", language='alias')+ " (VE)",
    "Portugal": emojize(":portugal:", language='alias')+ " (PT)",
}
class Event(Enum):
    THREAT_FEED = 'NEW_POST'

class Category(Enum):
    RANSOMWARE = 'Ransomware'
    DDOS = 'DDoS Attack'
    MALWARE = 'Malware'
    PHISHING = 'Phishing'
    DATA_LEAK = 'Data Leak'
    COMBO_LIST = 'Combo List'
    DATA_BREACH = 'Data Breach'
    LOGS = 'Logs'
    DEFACEMENT = 'Defacement'
    ALERT = 'Alert'
    VULNERABILITY = 'Vulnerability'

country_victims = [
    'Antigua and Barbuda', 'Argentina', 'Bahamas', 'Barbados', 
    'Belize', 'Bolivia', 'Brazil', 'Canada', 'Chile', 'Colombia',
    'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'Ecuador',
    'El Salvador', 'Grenada', 'Guatemala', 'Guyana', 'Haiti', 'Honduras', 
    'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 
    'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines',
    'Suriname', 'Trinidad and Tobago', 'USA', 'Uruguay','Venezuela'
]

def emojize_countries(countries):
    emojis = []
    for country in countries:
        emojis.append(member_countries_emojis[country])
    return ', '.join(emojis)

def test_emojis():
    bot = telebot.TeleBot(TG_TOKEN_KEY)
    bot.send_message(CHAT_ID, emojize_countries(country_victims), parse_mode='HTML')

def enviar_incidente(token, chat_id, title, content, category, url, countries, threat_actors):
    bot = telebot.TeleBot(token)
    texto = emojize(":police_car_light:", language='alias') + \
        " <b>Nuevo Incidente de "+category+"</b> " + emojize(":police_car_light: \n", language='alias') \
            + "<b>Title</b>: " + title + "\n"\
            + "<b>Threat Actors</b>: " + threat_actors + "\n"\
            + "<b>Content</b>: " + content \
            + "\n<b>Países miembros afectados</b>: " + emojize_countries(countries) \
            + " \n<b>Publicado en</b>: <a href=\"" + url + "\">Link</a>"
    for x in telebot.util.smart_split(texto, 4096):
        bot.send_message(chat_id, texto, parse_mode='HTML')

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
        # print("Nuevo incidente de " + self.category + " en " + ', '.join(countries))
        if self.is_threat_feed_event() and self.is_ransomware() and countries != []:
            enviar_incidente(TG_TOKEN_KEY, CHAT_ID, self.title, self.content, self.category, self.url, countries, ', '.join(self.get_threat_actors()))
        else:
            return False
        return True


def verify_basic_auth(username, password):
    return username == USERNAME and password == PASSWORD


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


if __name__ == "__main__":
    app.run(port=port)
