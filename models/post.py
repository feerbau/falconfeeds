from database import db
from enums.category import Category
from models.threat_actor import ThreatActor

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(100))
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    category = db.Column(db.Enum(Category))
    network = db.Column(db.String(50))
    published_timestamp = db.Column(db.Integer)
    published_url = db.Column(db.String(200))
    
    images = db.relationship('Image', backref='post', lazy='dynamic')
    countries = db.relationship('Country', secondary='post_country_association', backref=db.backref('posts', lazy='dynamic'))
    industries = db.relationship('Industry', secondary='post_industry_association', backref=db.backref('posts', lazy='dynamic'))
    sites = db.relationship('Site', secondary='post_site_association', backref=db.backref('posts', lazy='dynamic'))
    threat_actors = db.relationship('ThreatActor', secondary='post_threatactor_association', backref=db.backref('posts', lazy='dynamic'))
    organizations = db.relationship('Organization', secondary='post_organization_association', backref=db.backref('posts', lazy='dynamic'))

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
