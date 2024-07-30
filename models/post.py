from database import db
from enums.category import Category
from models.threat_actor import ThreatActor
from models.site import Site
from models.industry import Industry
from models.country import Country
from models.organization import Organization
from models.image import Image
from utils import country_victims
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(100))
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    category = db.Column(db.Enum(Category))
    network = db.Column(db.String(50))
    triggered_at = db.Column(db.DateTime)
    published_timestamp_miliseconds = db.Column(db.BigInteger)
    published_at = db.Column(db.Date)
    published_url = db.Column(db.String(200))

    images = db.relationship('Image', backref='post', lazy='dynamic')
    countries = db.relationship('Country', secondary='post_country_association', backref=db.backref('posts', lazy='dynamic'))
    industries = db.relationship('Industry', secondary='post_industry_association', backref=db.backref('posts', lazy='dynamic'))
    sites = db.relationship('Site', secondary='post_site_association', backref=db.backref('posts', lazy='dynamic'))
    threat_actors = db.relationship('ThreatActor', secondary='post_threatactor_association', backref=db.backref('posts', lazy='dynamic'))
    organizations = db.relationship('Organization', secondary='post_organization_association', backref=db.backref('posts', lazy='dynamic'))

    @classmethod
    def create(self, **kwargs):
        attrs = {
            'uuid': kwargs['data']['uuid'],
            'triggered_at': datetime.strptime(kwargs['eventTriggeredAt'], "%Y-%m-%dT%H:%M:%SZ"),
            'category': Category(kwargs['data']['category']),
            'published_timestamp_miliseconds': kwargs['data']['publishedTimestampInMilliseconds'],
            # 'threat_actors': kwargs['data']['threatActors'],
            # 'victims': kwargs['data']['victims'],
            'network': kwargs['data']['network'],
            'title': kwargs['data']['title'],
            'content': kwargs['data']['content'],
            'published_url': kwargs['data']['publishedURL']
        }
        attrs['published_at'] = datetime.fromtimestamp(attrs['published_timestamp_miliseconds'] / 1000).date()
        post = Post(**attrs)
        db.session.add(post)
        db.session.commit()
        return post

    @classmethod
    def update_rels(self, post, **kwargs):
        victims = kwargs['data']['victims']
        post.countries, post.industries, post.sites, post.organizations, post.images, post.threat_actors = [], [], [], [], [], []
        for victim in victims:
            if victim['type'] == 'Country':
                for raw_country in victim['values']:
                    if raw_country in country_victims:
                        country = Country.get_or_create(raw_country)
                        post.countries.append(country)
            if victim['type'] == 'Industry':
                for raw_industry in victim['values']:
                    industry = Industry.get_or_create(raw_industry)
                    post.industries.append(industry)
            if victim['type'] == 'Organization':
                for raw_organization in victim['values']:
                    organization = Organization.get_or_create(raw_organization)
                    post.organizations.append(organization)
            if victim['type'] == 'Site':
                for raw_site in victim['values']:
                    site = Site.get_or_create(raw_site)
                    post.sites.append(site)

        for raw_threat_actor in kwargs['data']['threatActors']:
            threat_actor = ThreatActor.get_or_create(**raw_threat_actor)
            post.threat_actors.append(threat_actor)

        db.session.add(post)
        db.session.commit()
        return post


post_organization_association = db.Table('post_organization_association',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('organization_id', db.Integer, db.ForeignKey('organization.id'))
)
post_country_association = db.Table('post_country_association',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('country_id', db.Integer, db.ForeignKey('country.id'))
)
post_industry_association = db.Table('post_industry_association',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('industry_id', db.Integer, db.ForeignKey('industry.id'))
)
post_site_association = db.Table('post_site_association',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('site_id', db.Integer, db.ForeignKey('site.id'))
)
post_threatactor_association = db.Table('post_threatactor_association',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('threatactor_id', db.Integer, db.ForeignKey(ThreatActor.id))
)
