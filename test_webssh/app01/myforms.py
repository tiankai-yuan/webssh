import time

from django import forms
from django.core.exceptions import ValidationError


def validate_even(value):
    # 不会生效， 因为原始的检验就回去看数据是否存在
    if not value:
        raise ValidationError('%s is not allow be null' % value)


class LogCommandForm(forms.Form):
    terminal_id = forms.CharField(validators=[validate_even])

