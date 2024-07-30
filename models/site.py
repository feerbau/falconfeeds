from database import db

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    @classmethod
    def get_or_create(self, name):
        site = Site.query.filter_by(name=name).first()
        if site is None:
            site = Site(name=name)
            db.session.add(site)
            db.session.commit()
        return site
