# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core import serializers
from django.http import JsonResponse
from todolist.decorators import dispatch_task
from todolist.models import Category, Task, FailedTask, User, Post, Group
from todolist.tasks import adding_task, insert_users_task
import logging
import math
from datetime import datetime
logger = logging.getLogger(__name__)
from django.db import connection


class HomePageView(View):
	def get(self, request):
		context = RequestContext(request)

		total = 20000
		chunk = 500

		perPage = math.ceil(total/chunk);

		def run_task(i, chunk):
			task = insert_users_task.delay(i, chunk)

		for x in range(perPage):
			dispatch_task(run_task(x, chunk))

		return render_to_response('todolist/index.html', {}, context)

def create_groups(request):
	for x in range(300):
		now = datetime.now()
		Group.objects.create(
			name="First Name 01", 
			phone="1232354",
			email='test' + str(x) + '@test.com',
			city="Skopje",
			created_at=now,
			updated_at=now,
		)
	return JsonResponse([], safe=False)	

def get_users(request):
    users = User.objects.select_related('group').prefetch_related("posts").order_by('-id')[:50].all()

    data = list(map(lambda user: {
		'user_id': user.id,
		'first_name': user.first_name,
		'last_name': user.last_name,
		'email': user.email,
		'age': user.age,
		'group': {
			'name': user.group.name,
			'phone': user.group.phone,
			'email': user.group.email,
			'city': user.group.city,
		},
		'posts': list(map(lambda post: {'title': post.title, 'content': post.content}, user.posts.all()))
    	}, users))

    # print(connection.queries)
    logger.error('number of users: ' + str(len(users)))

    # data = serializers.serialize('json', data)
    # return HttpResponse(data, content_type="application/json")	
    return JsonResponse(data, safe=False)	


class CategoryList(ListView):
	queryset = Category.objects.order_by('-name')


class CategoryDetailView(DetailView):
	model = Category
	template_name = 'todolist/category_detail.html'
	context_object_name = 'category'


class CategoryCreate(CreateView):
	model = Category
	fields = ('name',)
	template_name = 'todolist/category_create.html'


class CategoryUpdate(UpdateView):
	model = Category
	fields = ('name',)
	template_name = 'todolist/category_update.html'
	context_object_name = 'category'


class CategoryDelete(DeleteView):
	model = Category


class TaskCreate(CreateView):
	model = Task
	fields = ('description', 'category', 'start_date',)
	template_name = 'todolist/task_create.html'

	def post(self, request, *args, **kwargs):

		response = super(TaskCreate, self).post(self, request, *args, **kwargs)

		def run_task():
			task = adding_task.delay(1)

		dispatch_task(run_task())

		return response


class TaskUpdate(UpdateView):
	model = Task
	fields = ('description', 'category', 'start_date',)
	template_name = 'todolist/task_update.html'
	context_object_name = 'task'

	def post(self, request, *args, **kwargs):

		response = super(TaskUpdate, self).post(self, request, *args, **kwargs)

		def run_task():
			task = adding_task.delay(1)

		dispatch_task(run_task())

		return response


class FailedTasks(View):
	def get(self, request):
		tasks = FailedTask.objects.all()

		def run_task(id):
			task = adding_task.delay(id)

		for task in tasks:
			dispatch_task(run_task(task.category_id), task.category_id)

		return HttpResponse('OK')







