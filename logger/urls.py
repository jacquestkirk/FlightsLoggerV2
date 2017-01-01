from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^testDb', views.testDb, name='testDb'),
    url(r'^showDb', views.showDb, name='showDb'),
    url(r'^queryCheapestFlight', views.QueryCheapestFlights, name='queryCheapestFlight')
]