from __future__ import absolute_import

from todolist.decorators import dispatch_task
from todolist.models import Category, Task


class Notifier:
	category = None

	def __init__(self, category_id):
		self.category = Category.objects.get(id=int(category_id))

	def create_auto_task(self):
		"""
		On each create or update a task create new auto-generated one
		:return:
		"""
		if self.category is not None:
			Task.objects.create(description="auto generated", start_date="2019-11-13 23:23", category=self.category)

	def send_mail(self):
		# to-do
		pass

	@staticmethod
	def auto_task(category_id):
		"""
		Create an instance of this class and call the logic for when task is created or updated
		:param category_id:
		:return:
		"""
		service = Notifier(category_id)
		service.create_auto_task()
		service.send_mail()


