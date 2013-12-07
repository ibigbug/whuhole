from wtforms import TextField, PasswordField, BooleanField
from wtforms import TextAreaField
from flask.ext.wtf.html5 import EmailField, URLField
from wtforms.validators import DataRequired, Email, Length, Regexp
from wtforms.validators import Optional, URL
from wtforms.validators import StopValidation

from flask.ext.babel import lazy_gettext as _

from ._base import BaseForm
from ..models import Account


__all__ = [
    'SignupForm', 'SigninForm', 'SettingForm'
]


class SignupForm(BaseForm):
    username = TextField(
        'Username', validators=[
            DataRequired(), Length(min=3, max=20),
            Regexp(r'^[a-z0-9A-Z]+$')
        ], description='English and numbers only')
    email = EmailField(
        'Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password', validators=[DataRequired()])

    def validate_username(self, field):
        data = field.data.lower()
        if Account.query.filter_by(username=data).count():
            raise ValueError('This name has been used')

    def validate_email(self, field):
        if Account.query.filter_by(email=field.data.lower()).count():
            raise ValueError('This email has been used')

    def save(self, role=None):
        user = Account(**self.data)
        if role:
            user.role = role
        user.save()
        return user


class SigninForm(BaseForm):
    account = TextField(
        'Account',
        validators=[DataRequired()],
        description='Username or Email'
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )

    permanent = BooleanField('Remenber me for a month')

    def validate_account(self, field):
        account = self.account.data.lower()
        if '@' in account:
            user = Account.query.filter_by(email=account).first()
        else:
            user = Account.query.filter_by(username=account).first()
        if not user:
            raise StopValidation(message=_('Account not Exists'))

    def validate_password(self, field):
        account = self.account.data.lower()
        if '@' in account:
            user = Account.query.filter_by(email=account).first()
        else:
            user = Account.query.filter_by(username=account).first()
        if not user:
            return
        if user.check_password(field.data):
            return
        raise StopValidation(message=_('Wrong Password'))


class SettingForm(BaseForm):
    screen_name = TextField(
        'Display Name',
        validators=[Length(max=30)])

    website = URLField(
        'Website',
        validators=[URL(), Optional()])

    city = TextField(
        'City',
        description=('Where are you living'))

    description = TextAreaField(
        'Description',
        validators=[Optional(), Length(max=400)],
        description='Markdown supported')
