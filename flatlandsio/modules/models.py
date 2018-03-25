from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    # flask-Login required methods
    @property
    def is_active(self):
        return True


    @property
    def is_authenticated(self):
        return True


    @property
    def is_anonymous(self):
        return False


    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __repr__(self):
        return f'<User {self.id}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.Column(db.String())
    tags = db.Column(db.String())
    strap = db.Column(db.String())
    content = db.Column(db.String())
    pub_date = db.Column(db.String())
    published = db.Column(db.Boolean, default=False)

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