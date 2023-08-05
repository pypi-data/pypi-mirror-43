from flask_wtf import Form
from flask_security.forms import password_required, password_length, EqualTo
from flask_security.utils import verify_and_update_password, encrypt_password
from wtforms import PasswordField
from oy.babel import lazy_gettext, gettext


class OyChangePasswordForm(Form):
    old_password = PasswordField(
        label=lazy_gettext("Old Password"),
        validators=[password_required],
        render_kw=dict(required=True),
    )
    password = PasswordField(
        label=lazy_gettext("Password"),
        description=lazy_gettext("Not less than 6 characters"),
        validators=[password_required, password_length],
        render_kw=dict(required=True),
    )
    password_confirm = PasswordField(
        label=lazy_gettext("Re-Type Password"),
        validators=[EqualTo("password", message="RETYPE_PASSWORD_MISMATCH")],
        render_kw=dict(required=True),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(OyChangePasswordForm, self).__init__(*args, **kwargs)

    def validate(self):
        if not super(OyChangePasswordForm, self).validate():
            return False
        if not verify_and_update_password(self.old_password.data, self.user):
            self.old_password.errors.append(gettext("Incorrect Password"))
            return False
        if self.old_password.data.strip() == self.password.data.strip():
            self.password.errors.append(
                gettext("The new password is the same as the old password")
            )
            return False
        return True


def change_password(user, password):
    user.password = encrypt_password(password)
