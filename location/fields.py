from django_case_insensitive_field import CaseInsensitiveFieldMixin
from django.db.models import CharField


class LowerCharField(CaseInsensitiveFieldMixin, CharField):

    def __init__(self, *args, **kwargs):
        super(CaseInsensitiveFieldMixin, self).__init__(*args, **kwargs)