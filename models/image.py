from database import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(100))
    base64 = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
