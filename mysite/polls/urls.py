from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    # /polls/
    url(r'^$', views.index, name='index'),

    # /polls/5
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),

    # /polls/5/results
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='result'),

    # /polls/5/votes
    url(r'^(?P<question_id>[0-9]+)/votes/$', views.vote, name='vote'),

]