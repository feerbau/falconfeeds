from database import db

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    @classmethod
    def get_or_create(self, name):
        organization = Organization.query.filter_by(name=name).first()
        if organization is None:
            organization = Organization(name=name)
            db.session.add(organization)
            db.session.commit()
        return organization
