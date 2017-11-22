# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
from datetime import datetime

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
	def validatelogin(self, post_data):
		errors = []

		if len(self.filter(email=post_data['email'])) > 0:

			user = self.filter(email=post_data['email'])[0]
			if not bcrypt.checkpw(post_data['password'].encode(),user.password.encode()):
				errors.append('email/password incorrect')
		else:
			errors.append('email/password incorrect')
		if errors:
			return errors
		return user

	def validateregistration(self, post_data):
		errors = []

		if len(post_data['name']) < 2 or len(post_data['username']) < 2:
			errors.append('name fields must be at least 3 characaters')

		if len(post_data['password']) < 8:
			errors.append('password must be at least 8 charcters')

		if not re.match(NAME_REGEX, post_data['name']):
			errors.append('name field must be alpha characters only')

		if not re.match(EMAIL_REGEX, post_data['email']):
			errors.append('invalid email format')
		if len(User.objects.filter(email=post_data['email'])) > 0:
			errors.append('email already in use')
		if post_data['password'] != post_data['password_confirm']:
			errors.append('passwords do not match')
		try:
			current_date = datetime.datetime.strptime(str(datetime.date.today()),'%Y-%m-%d')
			user_datehired = datetime.datetime.strptime(str(datetime.date.post_data['datehired','%Y-%m-%d']))
			if user_datehired > current_date:
				errors.append('Sorry time traveler, you must have a birthday earlier than today!')
		except:
				pass

		if not errors:

			hashed= bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

			new_user = self.create(
				name = post_data['name'],
				username = post_data['username'],
				email = post_data['email'],
				password = hashed,
				datehired = post_data['datehired']
			)
			return new_user#(True, new_user)
		return errors#(False,errors)

class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=255)
	datehired = models.DateField()
	objects = UserManager()

	def __str__(self):
		return self.email

class WishManager(models.Manager):
	def validatewish(self,post_data):
		errors = []
		for key in post_data:
			if post_data[key] =='':
				errors.append('All fields must be filled!')
				return errors
		if len(post_data['product']) < 3:
			errors.append('Product name must be longer than 3 characters.')
		
		return errors


class Wish(models.Model):
	product = models.CharField(max_length=255)
	created_at = models.DateField(auto_now_add=True)
	wisher = models.ForeignKey(User, related_name='iwish')
	wishes = models.ManyToManyField(User, related_name='youwish')
	objects = WishManager()