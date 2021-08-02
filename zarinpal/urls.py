from django.conf.urls import url
from . import views
from django.urls import path


app_name = 'zarinpal'

urlpatterns = [
    url(r'^request/$', views.send_request, name='request'),
    url(r'^verify/$', views.verify , name='verify'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
]
