import functools

from django.utils import timezone

from todolist.models import FailedTask


def dispatch_task(func=None, category_id = None):
	"""Automatically silence any errors that occur within a function"""

	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			except Exception as e:
				# keep the task in database for cron loop in case redis was done
				FailedTask.objects.create(category_id=category_id, description=str(e), failed_at=timezone.now())

		return wrapper

	if func is None:
		return decorator
	else:
		return decorator(func)
