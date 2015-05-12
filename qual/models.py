import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from qual import db

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
	nickname = db.Column(db.String(64), index=True, unique=True)
        realname = db.Column(db.String(64))
	password = db.Column(db.String(256))
	score = db.Column(db.Integer)
	admin = db.Column(db.Boolean)
	solves = db.relationship('Problem', secondary=solves, backref=db.backref('solvers', lazy='dynamic'), lazy='dynamic')
	updated_at = db.Column(db.DateTime)

	def __init__(self, username, nickname, password, admin=False):
		self.username = username
		self.nickname = nickname
		self.set_password(password)
		self.score = 0
		self.admin = admin
		self.updated_at = datetime.datetime.utcnow()

	def __repr__(self):
		return '<User %s %s>' % (self.username, self.nickname)

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
		self.updated_at = datetime.datetime.utcnow()
		self.score += problem.score
		self.solves.append(problem)
		for problemset in problem.problemsets:
			score = ProblemSetScore.query.filter_by(problemset_id=problemset.id, user_id=self.id).first()
			if not score:
				score = ProblemSetScore(problemset, self)
				db.session.add(score)
			score.score += problem.score
			score.updated_at = datetime.datetime.utcnow()

	def build_score(self):
		self.score = 0
		for problem in self.solves:
			self.score += problem.score

class Problem(db.Model):
	__tablename__ = 'problem'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64), index=True, unique=True)
	content = db.Column(db.UnicodeText)
	flag = db.Column(db.String(256))
	score = db.Column(db.Integer)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	category_name = db.Column(db.String(64))

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

	def __init__(self, name=''):
		self.name = name
		self.problems_count = 0

	def __repr__(self):
		return '<Category %s>' % (self.name)

class ProblemSet(db.Model):
	__tablename__ = 'problemset'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64), index=True, unique=True)
	problems = db.relationship('Problem', secondary=includes, backref=db.backref('problemsets', lazy='dynamic'), lazy='dynamic')
	problems_count = db.Column(db.Integer)

	def __repr__(self):
		return '<ProblemSet %s>' % (self.title)

	def build_score(self):
		for score in ProblemSetScore.query.filter_by(problemset_id=self.id).all():
			db.session.delete(score)
		total = {}
		for problem in self.problems:
			for solver in problem.solvers:
				if not solver in total:
					total[solver] = 0
				total[solver] += problem.score
		for solver in total:
			score = ProblemSetScore(self, solver, total[solver])
			db.session.add(score)

class ProblemSetScore(db.Model):
	__tablename__ = 'problemsetscore'
	id = db.Column(db.Integer, primary_key=True)
	problemset_id = db.Column(db.Integer, db.ForeignKey('problemset.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	nickname = db.Column(db.String(64))
	score = db.Column(db.Integer)
	updated_at = db.Column(db.DateTime)

	def __init__(self, problemset, user, score=0):
		self.problemset_id = problemset.id
		self.user_id = user.id
		self.nickname = user.nickname
		self.score = score
		self.updated_at = datetime.datetime.utcnow()
