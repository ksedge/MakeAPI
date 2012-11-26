from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from uuid import UUID


def validate_uuid (value):
    if not isinstance(value, UUID):
        try:
            UUID(value)
        except ValueError:
            raise ValidationError(_(u'%s is not a recognizable UUID' % value))
