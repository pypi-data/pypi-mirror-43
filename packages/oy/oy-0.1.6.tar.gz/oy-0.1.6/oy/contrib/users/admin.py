# -*- coding: utf-8 -*-
"""
    oy.contrib.users.admin
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Provides the users management admin interface.

    :copyright: (c) 2018 by Musharraf Omer.
    :license: MIT, see LICENSE for more details.
"""

from wtforms.fields import StringField, PasswordField, FileField
from flask import current_app, request, url_for, flash, redirect, abort
from flask_security import current_user
from flask_security.changeable import change_user_password
from flask_security.registerable import register_user
from flask_security.utils import hash_password, verify_password
from flask_admin.form import rules
from flask_admin import expose
from oy.boot.sqla import db
from oy.boot.security import user_datastore
from oy.boot.flask_security_forms import OyRegisterForm
from oy.babel import gettext, lazy_gettext
from oy.models.user import User
from oy.dynamicform import DynamicForm
from oy.contrib.admin import OyModelView
from .models import ProfileExtras


# Used to make the field names of user profile unique
_prefix = "profile_extra__"
_wrap_field = lambda name: _prefix + name
_unwrap_field = lambda name: name[len(_prefix) :]


class UserAdmin(OyModelView):
    column_list = ["user_name", "email", "active"]
    form_excluded_columns = ("password", "confirmed_at", "profile")

    def is_accessible(self):
        if super().is_accessible():
            if current_user.has_role("admin"):
                return True
            elif request.endpoint.endswith(".edit_view") and ("id" in request.args):
                user = self.get_one(request.args["id"])
                if user is current_user._get_current_object():
                    return True
        return False

    def edit_form(self, obj):
        form = super().edit_form(obj)
        to_delete = ("roles", "active")
        for d in to_delete:
            if (d in form) and not current_user.has_role("admin"):
                del form[d]
        return form

    def validate_form(self, form):
        user = self.get_one(request.args["id"])
        if "active" in form and user.id == current_user.id and not form.active.data:
            flash(gettext("You can not deactivate your own account."))
            return False
        if not form["old_password"].data:
            return super().validate_form(form)
        if not user:
            flash(gettext("User does not exist."), category="error")
            return False
        o, n, c = [
            form[f].data
            for f in ("old_password", "new_password", "new_password_confirm")
        ]
        if not verify_password(o, user.password):
            flash(
                gettext("The password you have entered is incorrect."), category="error"
            )
            return False
        elif o and not any([n, c]):
            flash(gettext("A new password was not provided."), category="warning")
            return False
        elif n != c:
            flash(gettext("Passwords do not match."), category="error")
            return False
        return True

    def after_model_change(self, form, model, is_created):
        if form["new_password"].data:
            if not current_app.debug:
                change_user_password(model, form["new_password"].data)
            else:
                model.password = hash_password(form["new_password"].data)
                db.session.commit()
            flash(gettext("The password has been changed successfully."))
        for field in (f for f in form if f.name.startswith(_prefix)):
            fname = _unwrap_field(field.name)
            if fname not in model.profile:
                model.profile.extras[fname] = ProfileExtras(key=fname)
            model.profile[fname] = field.data
        db.session.commit()

    def get_form(self):
        form = super().get_form()
        rv = dict(
            old_password=PasswordField(label=lazy_gettext("Old Password")),
            new_password=PasswordField(label=lazy_gettext("New Password")),
            new_password_confirm=PasswordField(
                label=lazy_gettext("Confirm New Password")
            ),
        )
        idarg = None if not request else request.args.get("id")
        user = None if not idarg else self.get_one(idarg)
        for fn, cf, kw in self.get_profile_fields():
            if user is not None:
                kw["default"] = user.profile.get(fn)
            rv[_wrap_field(fn)] = cf(**kw)
        for k, v in rv.items():
            setattr(form, k, v)
        return form

    @property
    def form_rules(self):
        rv = [
            "user_name",
            "email",
            rules.NestedRule(
                [
                    rules.HTML("<h4>" + lazy_gettext("Change Password") + "</h4>"),
                    "old_password",
                    "new_password",
                    "new_password_confirm",
                ]
            ),
            rules.HTML("<h4>" + lazy_gettext("Profile Details") + "</h4>"),
        ]
        for fn, _, __ in self.get_profile_fields():
            rv.append(_wrap_field(fn))
        if current_user.has_role("admin"):
            rv.extend(["active", "roles"])
        return rv

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for("admin.index"))

    def get_profile_fields(self):
        """Contribute the fields of profile extras"""
        profile_fields = current_app.data["profile_fields"]
        yield from DynamicForm(profile_fields).fields

    @expose("/register", methods=("GET", "POST"))
    def create_view(self):
        template = self.create_template
        form = OyRegisterForm()
        if form.validate():
            if not current_app.debug:
                register_user(**form.to_dict())
            else:
                user_data = form.to_dict()
                user_datastore.create_user(
                    user_name=user_data["user_name"],
                    email=user_data["email"],
                    password=hash_password(user_data["password"]),
                    roles=user_data["roles"],
                )
                db.session.commit()
            flash(gettext("User created successfully."))
            return redirect(url_for(".index_view"))
        return self.render(template, form=form)


def register_admin(app, admin):
    admin.add_view(
        UserAdmin(
            User,
            db.session,
            name=lazy_gettext("user account"),
            verbose_name=lazy_gettext("user accounts"),
            endpoint="users",
            menu_icon_type="fa",
            menu_icon_value="fa-users",
            menu_order=100,
        )
    )
