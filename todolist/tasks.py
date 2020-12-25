from __future__ import absolute_import

from celery import shared_task
from datetime import datetime

from todolist.services import Notifier
from todolist.models import User, Post, Group


@shared_task # Use this decorator to make this a asynchronous function
def adding_task(cat_id):
    Notifier.auto_task(cat_id)

@shared_task
def insert_users_task(i, chunk):
	offset = i * chunk
	group = Group.objects.get(pk=200)
	for s in range(chunk):
		now = datetime.now()
		t = offset + s;

		user = User.objects.create(
			first_name="First Name 01",
			last_name="First Name 01",
			email='test' + str(t) + '@test.com',
			age=t,
			group=group,
			created_at=now,
			updated_at=now,
		)

		Post.objects.create(
			title="auto generated", 
			content="auto generated", 
			user=user,
			created_at=now,
			updated_at=now,
		)
		Post.objects.create(
			title="auto generated", 
			content="auto generated", 
			user=user,
			created_at=now,
			updated_at=now,
		)



	

