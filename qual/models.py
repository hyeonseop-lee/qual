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

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(256))
    score = db.Column(db.Integer)
    admin = db.Column(db.Boolean)
    solves = db.relationship('Problem', secondary=solves, backref=db.backref('solvers', lazy='dynamic'), lazy='dynamic')

    def __init__(self, username, password, admin=False):
        self.username = username
        self.set_password(password)
        self.score = 0
        self.admin = admin

    def __repr__(self):
        return '<User %s>' % (self.username, )

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

    def solved(self, problem):
        return db.session.query(solves).filter_by(user_id=self.id, problem_id=problem.id).first()

    def solve(self, problem):
        self.score += problem.score
        self.solves.append(problem)
        for problemset in problem.problemsets:
            score = ProblemSetScore.query.filter_by(problemset_id=problemset.id, user_id=self.id).first()
            if not score:
                score = ProblemSetScore(problemset, self)
                db.session.add(score)
            score.score += problem.score
        db.session.commit()

class Problem(db.Model):
    __tablename__ = 'problem'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    content = db.Column(db.UnicodeText)
    flag = db.Column(db.String(256))
    score = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category_name = db.Column(db.String(64))

    def __init__(self, title, content, flag, score, category):
        self.title = title
        self.content = content
        self.flag = flag
        self.score = score
        category.append(self)
        self.category_name = category.name

    def __repr__(self):
        return '<Problem %s%d %s>' % (self.category_name, self.score, self.title)

    def check_flag(self, flag):
        return self.flag == flag

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    problems = db.relationship('Problem', backref='category', lazy='dynamic')
    problems_count = db.Column(db.Integer)

    def __init__(self, name):
        self.name = name
        self.problems_count = 0

    def __repr__(self):
        return '<Category %s>' % (self.name)

    def append(self, problem):
        self.problems.append(problem)
        self.problems_count += 1

class ProblemSet(db.Model):
    __tablename__ = 'problemset'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    problems = db.relationship('Problem', secondary=includes, backref=db.backref('problemsets', lazy='dynamic'), lazy='dynamic')
    problems_count = db.Column(db.Integer)

    def __init__(self, title):
        self.title = title
        self.problems_count = 0

    def __repr__(self):
        return '<ProblemSet %s>' % (self.title)

    def append(self, problem):
        self.problems.append(problem)
        self.problems_count += 1

class ProblemSetScore(db.Model):
    __tablename__ = 'problemsetscore'
    id = db.Column(db.Integer, primary_key=True)
    problemset_id = db.Column(db.Integer, db.ForeignKey('problemset.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(64))
    score = db.Column(db.Integer)

    def __init__(self, problemset, user):
        self.problemset_id = problemset.id
        self.user_id = user.id
        self.username = user.username
        self.score = 0
