# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
# Create your views here.

def index(request):
	if 'user_id' in request.session:
		return redirect('/dashboard')
	return render(request, 'first_app/index.html')

def register(request):
	result = User.objects.validateregistration(request.POST)
	if type(result) == list:
		for err in result:
			messages.error(request, err)
		return redirect('/')
	request.session['user_id'] = result.id
	messages.success(request,'Successfully registered')
	return redirect('/dashboard')

def login(request):
	if 'user_id' in request.session:
		return redirect('/dashboard')
	result = User.objects.validatelogin(request.POST)
	if type(result) == list:
		for err in result:
			messages.error(request, err)
		return redirect('/')
	request.session['user_id'] = result.id
	messages.success(request, "Successfully logged in!")
	return redirect('/dashboard')

def logout(request):
	request.session.clear()
	return redirect('/')

def show(request):
	try:
		request.session['user_id']
	except KeyError:
		return redirect('/')

	user = User.objects.get(id=request.session['user_id'])
	context = {
		'user': user,
		'mywishes': Wish.objects.all().filter(wishes=user), #user.iwish.all(),
		'wishes': Wish.objects.all().exclude(wishes=user)
	}
	return render(request, 'first_app/dashboard.html', context)
def add(request):
	try:
		request.session['user_id']
	except KeyError:
		return redirect('/')

	return render(request, 'first_app/add.html')

def wish(request, id):
	try:
		request.session['user_id']
	except KeyError:
		return redirect('/')

	wish = Wish.objects.get(id=id)
	user = User.objects.get(id=request.session['user_id'])
	context = {
		'wish': wish,
		'wishlist': user.iwish.all(),
	}
	return render(request,'first_app/wish_items.html', context)
def create(request):
	errs = Wish.objects.validatewish(request.POST)
	if errs:
		for e in errs:
			messages.error(request, e)
		return redirect('/dashboard')
	user = User.objects.get(id=request.session['user_id'])
	wish = Wish.objects.create(
			product = request.POST['product'],
			wisher = user
		)
	return redirect('/dashboard')

def addwish(request,id):
	user = User.objects.get(id=request.session['user_id'])
	wish = Wish.objects.get(id=id)
	wish.wishes.add(user)
	wish.save()

	return redirect('/dashboard')

def remove(request, id):
	user = User.objects.get(id=request.session['user_id'])
	wish = Wish.objects.get(id=id)
	wish.wishes.remove(user)
	wish.save()

	return redirect('/dashboard') 
