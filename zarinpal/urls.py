from django.conf.urls import url
from . import views
from django.urls import path
from django.utils.translation import gettext_lazy as _


app_name = 'zarinpal'

urlpatterns = [
    url(r'^request/$', views.send_request, name='request'),
    url(r'^verify/$', views.verify , name='verify'),
    path(_('done/'), views.payment_done, name='done'),
    path(_('canceled/'), views.payment_canceled, name='canceled'),
]
