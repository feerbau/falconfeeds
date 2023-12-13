from database import db

class ThreatActor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(100))
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
