from django.conf.urls import url
import views

urlpatterns = [
    url(r'^currencies/(?P<pk>[0-9]+)/$', views.currency_rate_detail, name='currency_rate_detail'),
    url(r'^currencies/', views.currency_rate_list, name='currency_rate_list'),
    url(r'^convert/', views.currency_convert, name='currency_convert'),
]