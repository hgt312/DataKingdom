# -*- coding:utf-8 -*-

from django.conf.urls import url

from .views import UserInfoView, UserAttendView, UserSetPasswordView
from .views import UserSetEmailView, UserUploadView, UserDownloadView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name="info"),
    url(r'^set/email$', UserSetEmailView.as_view(), name="set_email"),
    url(r'^set/password$', UserSetPasswordView.as_view(), name="set_password"),
    url(r'^attend/$', UserAttendView.as_view(), name="attend"),

    url(r'^upload/$', UserUploadView.as_view(), name="upload"),
    url(r'^download/(?P<competition_id>\d+)/$', UserDownloadView.as_view(), name="download"),
]
