from database import db

class ThreatActor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(100))
    name = db.Column(db.String(100))
    description = db.Column(db.Text)

    @classmethod
    def get_or_create(self, **kwargs):
        threat_actor = ThreatActor.query.filter_by(uuid=kwargs['uuid']).first()
        if threat_actor is None:
            threat_actor = ThreatActor(uuid=kwargs['uuid'], name=kwargs['name'], description=kwargs['description'])
            db.session.add(threat_actor)
            db.session.commit()
        return threat_actor
