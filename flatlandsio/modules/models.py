from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.Column(db.String())
    tags = db.Column(db.String())
    strap = db.Column(db.String())
    content = db.Column(db.String())
    pub_date = db.Column(db.String())
    published = db.Column(db.String())

    def __repr__(self):
        return '<Post %r>' % self.title


class Software(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.Column(db.String())
    tags = db.Column(db.String())
    strap = db.Column(db.String())
    content = db.Column(db.String())
    type = db.Column(db.String())

    def __repr__(self):
        return '<Software %r>' % self.title