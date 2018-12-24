from django.conf.urls import url
import views

urlpatterns = [
    url('currencies/', views.currency_rate_list),
    url('currencies/<int:pk>/', views.currency_rate_detail),
]