# -*- coding: utf-8 -*-
"""
    oy.contrib.page
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Provides a simple page that have a rich-text  field.

    :copyright: (c) 2018 by Musharraf Omer.
    :license: MIT, see LICENSE for more details.
"""

from oy.views import ContentView
from oy.babel import lazy_gettext
from oy.contrib.extbase import OyExtBase
from . import models
from .admin import register_admin


class RichTextPageView(ContentView):
    """Default view for `richtext_page` content type."""


class RichTextPage(OyExtBase):

    module_args = dict(
        name="oy.contrib.richtext_page",
        import_name="oy.contrib.richtext_page",
        template_folder="templates",
        viewable_name=lazy_gettext("Rich Text Page"),
    )

    def init_app(self, app):
        app.add_contenttype_handler("richtext_page", RichTextPageView)
