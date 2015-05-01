from qual import db
from werkzeug.security import generate_password_hash, check_password_hash

solves = db.Table('solves',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('problem_id', db.Integer, db.ForeignKey('problem.id'))
)

includes = db.Table('includes',
        db.Column('problemset_id', db.Integer, db.ForeignKey('problemset.id')),
        db.Column('problem_id', db.Integer, db.ForeignKey('problem.id'))
)

scores = db.Table('scores',
        db.Column('problemset_id', db.Integer, db.ForeignKey('problemset.id')),
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('username', db.String(64)),
        db.Column('score', db.Integer)
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(256))
    score = db.Column(db.Integer, default=0)
    admin = db.Column(db.Boolean, default=False)
    solves = db.relationship('Problem', secondary=solves, backref=db.backref('solvers', lazy='dynamic'), lazy='dynamic')

    def __init__(self, username, password, admin=False):
        self.username = username
        self.set_password(password)
        self.admin = admin

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

class Problem(db.Model):
    __tablename__ = 'problem'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    content = db.Column(db.UnicodeText)
    flag = db.Column(db.String(256))
    score = db.Column(db.Integer)
    category_name = db.Column(db.String(64), db.ForeignKey('category.name'))

    def check_flag(self, flag):
        return self.flag == flag

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    problems = db.relationship('Problem', backref='category', lazy='dynamic')
    problems_count = db.Column(db.Integer, default=0)

class ProblemSet(db.Model):
    __tablename__ = 'problemset'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.UnicodeText)
    problems = db.relationship('Problem', secondary=includes, backref=db.backref('problemsets', lazy='dynamic'), lazy='dynamic')
    problems_count = db.Column(db.Integer, default=0)
