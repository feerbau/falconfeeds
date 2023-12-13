from config import Config
from enums.category import Category
from enums.event import Event
from utils import (
    enviar_incidente,
    country_victims,
)

class FalconFeedsService:
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
            enviar_incidente(Config.TG_TOKEN_KEY, Config.CHAT_ID, self.title, self.content, self.category, self.url, countries, ', '.join(self.get_threat_actors()))
        else:
            return False
        return True
