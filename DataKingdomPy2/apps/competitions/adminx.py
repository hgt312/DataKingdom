# -*- coding:utf-8 -*-

import xadmin

from .models import Competition, AttendedPerson


class CompetitionAdmin(object):
    list_display = ['name', 'is_team', 'start_date', 'end_date', 'enroll_date', 'deadline']
    search_fields = ['name', 'organization']
    list_filter = ['name', 'start_date', 'end_date', 'enroll_date', 'deadline', 'organization', 'is_team']
    style_fields = {"detail": "ueditor"}


class AttendedPersonAdmin(object):
    list_display = ['competition', 'person']
    search_fields = ['competition', 'person']
    list_filter = ['competition', 'person']

xadmin.site.register(Competition, CompetitionAdmin)
xadmin.site.register(AttendedPerson, AttendedPersonAdmin)
