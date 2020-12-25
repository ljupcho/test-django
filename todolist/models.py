# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.db import models
from django.utils import timezone


class Group(models.Model):
	name= models.CharField(max_length=255)
	phone= models.CharField(max_length=255)
	email= models.EmailField(max_length=255, unique=True)
	city= models.CharField(max_length=255)
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()

class User(models.Model):
	first_name= models.CharField(max_length=255)
	last_name= models.CharField(max_length=255)
	email= models.EmailField(max_length=255, unique=True)
	age = models.IntegerField()
	group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name="group")
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()

class Post(models.Model):
	title= models.CharField(max_length=255)
	content = models.TextField()
	user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()

class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('category-detail', kwargs={'pk': self.pk})


class Task(models.Model):
	description = models.TextField(blank=False)
	start_date = models.DateTimeField()
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	created_at = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))

	def __str__(self):
		return self.description

	def get_absolute_url(self):
		return reverse('category-detail', kwargs={'pk': self.category.id})


class FailedTask(models.Model):
	description = models.TextField(blank=False)
	failed_at = models.DateTimeField()
	category_id = models.IntegerField(blank=True)

