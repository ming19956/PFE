from django.conf.urls import url
from . import views

app_name = 'frontend'
urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^classify$', views.classification, name='classify'),
    url(r'^crawl', views.crawl),
    url(r'^show', views.show),
    url(r'^filter',views.filter)
]