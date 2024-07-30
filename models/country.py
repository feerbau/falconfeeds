from database import db

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return '<Country %r>' % self.name
    
    @classmethod
    def get_or_create(self, name):
        country = Country.query.filter_by(name=name).first()
        if country is None:
            country = Country(name=name)
            db.session.add(country)
            db.session.commit()
        return country
