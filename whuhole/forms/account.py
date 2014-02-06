# coding: utf-8
from werkzeug import check_password_hash

from flask.ext.wtf import Form
from wtforms.fields import StringField
from wtforms.fields import PasswordField
from wtforms.fields import TextAreaField

from wtforms.validators import ValidationError

from ..models import Account


class AccountBaseForm(Form):
    username = StringField('Username')
    password = PasswordField('Passoword')


class RegisterForm(AccountBaseForm):
    def validate_username(self, field):
        u = Account.query.filter_by(username=field.data).first()
        if u:  # username exists
            raise ValidationError(u'用户名已经存在')


class LoginForm(AccountBaseForm):
    def validate_password(self, field):
        username = self.username.data
        password = field.data
        u = Account.query.filter_by(username=username).first()
        if not u:
            raise ValidationError(u'用户名不存在')
        if not check_password_hash(u.password, password):
            raise ValidationError(u'密码错误')
        self.user = u
        return u


class ProfileForm(Form):
    email = StringField(u'电子邮件')
    screen_name = StringField(u'昵称')
    location = StringField(u'居住地')
    website = StringField(u'个人主页')
    description = TextAreaField(u'个人简介')
