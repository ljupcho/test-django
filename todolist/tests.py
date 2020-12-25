# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from todolist.models import Category


class CategoryModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		Category.objects.create(name='test')

	def test_category_name(self):
		category = Category.objects.get(name='test')
		self.assertEqual(category.name, 'test')

	def test_get_absolute_url(self):
		category = Category.objects.get(name='test')
		self.assertEqual(category.get_absolute_url(), '/todolist/categories/'+ str(category.id) +'/')