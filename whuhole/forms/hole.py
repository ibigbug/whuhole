from flask import g

from wtforms import TextField
from wtforms.validators import DataRequired, Length

from _base import BaseForm

from ..models import Status

__all__ = ['StatusForm']


class StatusForm(BaseForm):
    content = TextField(
        ('Status'), validators=[
            DataRequired(), Length(min=3, max=280)
        ], description=('Length must between 3 and 280'))

    def save(self):
        status = Status(**self.data)
        status.account_id = g.user.id
        status.save()

        return status
