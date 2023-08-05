# -*- coding: utf-8 -*-
"""
    oy.contrib.redirects.admin
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Provides the admin interface for editing oy redirects.

    :copyright: (c) 2019 by Musharraf Omer.
    :license: MIT, see LICENSE for more details.
"""

from flask_security import current_user
from oy.models import db
from oy.babel import lazy_gettext
from oy.contrib.admin.wrappers import OyModelView
from .models import Redirect


class RedirectsAdmin(OyModelView):
    form_columns = ("from_url", "to_url", "to_page", "permanent")
    column_list = ("from_url", "to_url", "to_page", "permanent")
    column_editable_list = ("from_url", "to_url")

    def is_accessible(self):
        return super().is_accessible() and current_user.has_role("admin")


def register_admin(app, admin):
    admin.add_view(
        RedirectsAdmin(
            Redirect,
            db.session,
            name=lazy_gettext("redirect"),
            verbose_name=lazy_gettext("redirects"),
            menu_icon_type="fa",
            menu_icon_value="fa-refresh",
            menu_order=300,
        )
    )
