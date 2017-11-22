from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^register$', views.register),
	url(r'^dashboard$', views.show),
	url(r'^wish_item/add', views.add),
	url(r'^wish_item/create', views.create),
	url(r'^wish_item/(?P<id>\d+)$', views.wish),
	url(r'^addwish/(?P<id>\d+)$', views.addwish),
	url(r'^remove/(?P<id>\d+)$', views.remove)
]