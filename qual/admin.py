from flask.ext.login import current_user
from flask.ext.admin.contrib.sqla import ModelView

class AdminView(ModelView):
	def is_accessible(self):
		return current_user.admin

class UserView(AdminView):
	can_create = False
	column_list = ('username', 'score', 'admin')
	form_columns = ('username', 'admin')

class ProblemView(AdminView):
	column_list = ('title', 'category_name', 'score')
	form_columns = ('title', 'content', 'flag', 'category')

class CategoryView(AdminView):
	column_list = ('name', )
	form_columns = ('name', )

class ProblemSetView(AdminView):
	column_list = ('title', )
	form_columns = ('title', 'problems')

from qual import admin, db
from qual.models import User, Problem, Category, ProblemSet

admin.add_view(UserView(User, db.session))
admin.add_view(ProblemView(Problem, db.session))
admin.add_view(CategoryView(Category, db.session))
admin.add_view(ProblemSetView(ProblemSet, db.session))
