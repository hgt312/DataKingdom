# -*- coding:utf-8 -*-

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from xadmin.layout import Fieldset, Main, Side, Row
from django.utils.translation import ugettext as _

from .models import UserProfile


# 全站xadmin配置
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = "DataKingdom后台管理系统"
    site_footer = "DataKingdom"
    # menu_style = "accordion"

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)


class UserProfileAdmin(UserAdmin):
    list_display = ['username', 'email', 'mobile', 'gender', 'real_name']
    search_fields = ['username', 'email', 'mobile', 'gender', 'real_name', 'organization', 'city']
    list_filter = ['username', 'email', 'mobile', 'gender', 'real_name', 'organization', 'city']
    exclude = ['first_name', 'last_name']

    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('',
                             'username', 'password', 'email',
                             css_class='unsort no_title'
                             ),
                    Fieldset(_('Personal info'),
                             Row('real_name', 'gender'),
                             Row('mobile', 'identity'),
                             Row('organization', 'work'),
                             Row('year', 'city'),
                             'introduction'
                             ),
                    Fieldset(_('Permissions'),
                             'groups', 'user_permissions'
                             ),
                    Fieldset(_('Important dates'),
                             'last_login', 'date_joined'
                             ),
                ),
                Side(
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserAdmin, self).get_form_layout()

xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfileAdmin)
