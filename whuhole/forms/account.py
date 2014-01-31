from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError

from ..models import Account


class AccountBaseForm(Form):
    username = StringField('Username')
    password = PasswordField('Passoword')


class RegisterForm(AccountBaseForm):
    def validate_username(self, field):
        u = Account.query.filter_by(username=field.data).first()
        if u:  # username exists
            raise ValidationError('Username exists')


class LoginForm(AccountBaseForm):
    def validate_username(self, field):
        u = Account.query.filter_by(username=field.data).first()
        if not u:
            raise ValidationError('Invalid username or password')

        self.user = u

    def validate_password(self, field):
        if self.user.password != field.data:
            raise ValidationError('Invalid username or password')
