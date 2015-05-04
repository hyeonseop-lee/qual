from flask.ext.login import current_user
from flask.ext.admin.contrib.sqla import ModelView

from qual import admin, db
from qual.models import User, Problem, Category, ProblemSet, ProblemSetScore

class AdminView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated() and current_user.admin

class UserView(AdminView):
	can_create = False
	column_list = ('username', 'nickname', 'score', 'admin')
	form_columns = ('username', 'nickname', 'admin')

	def on_model_change(self, form, user, is_create):
		ProblemSetScore.query.filter_by(user_id=user.id).update({'nickname': user.nickname})

	def on_mode_delete(self, user):
		ProblemSetScore.query.filter_by(user_id=user.id).delete()

class ProblemView(AdminView):
	column_list = ('title', 'category_name', 'score')
	form_columns = ('title', 'content', 'flag', 'score', 'category')

	def on_model_change(self, form, problem, is_create):
		problem.category_name = problem.category.name
		for solver in problem.solvers:
			solver.build_score()
		for problemset in problem.problemsets:
			problemset.build_score()
		for category in Category.query.all():
			category.problems_count = len(category.problems.all())

	def on_model_delete(self, problem):
		for solver in problem.solvers:
			solver.solves.remove(problem)
			solver.build_score()
		for problemset in problem.problemsets:
			problemset.problems.remove(problem)
			problemset.problems_count -= 1
			problemset.build_score()
		problem.category.problems_count -= 1

class CategoryView(AdminView):
	column_list = ('name', )
	form_columns = ('name', )

class ProblemSetView(AdminView):
	column_list = ('title', )
	form_columns = ('title', 'problems')

	def on_model_change(self, form, problemset, is_create):
		problemset.problems_count = len(problemset.problems.all())
		problemset.build_score()

	def on_model_delete(self, problemset):
		ProblemSetScore.query.filter_by(problemset_id=problemset.id).delete()

admin.add_view(UserView(User, db.session))
admin.add_view(ProblemView(Problem, db.session))
admin.add_view(CategoryView(Category, db.session))
admin.add_view(ProblemSetView(ProblemSet, db.session))
