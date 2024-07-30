from database import db

class Industry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    @classmethod
    def get_or_create(self, name):
        industry = Industry.query.filter_by(name=name).first()
        if industry is None:
            industry = Industry(name=name)
            db.session.add(industry)
            db.session.commit()
        return industry
