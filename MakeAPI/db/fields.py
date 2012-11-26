from django.db.models import CharField
import uuid
import re
from . import validators


class UUIDVersionError (Exception):
    pass


class UUIDField (CharField):
    """ UUIDField

    By default uses UUID version 1 (generate from host ID, sequence number and current time)

    The field support all uuid versions which are natively supported by the uuid python module.
    For more information see: http://docs.python.org/lib/module-uuid.html
    """

    default_validators = [validators.validate_uuid,]

    def __init__ (self, verbose_name=None, name=None, auto=False, auto_update=False,
                  version=1, node=None, clock_seq=None, namespace=None, **kwargs):

        # Make sure we support the given version
        if version not in (1, 3, 4, 5):
            raise UUIDVersionError("UUID version %s is not supported." % version)

        if auto_update or kwargs.get('primary_key'):
            auto = True

        self.auto = auto
        self.auto_update = auto_update
        self.version = version

        kwargs['max_length'] = 36
        kwargs['unique'] = True # In theory, UUIDs should always be unique (!),
                                # but enforce it at DB level anyway
        if auto:
            # By default, if we're responsible for this field, don't let the user edit it
            kwargs.setdefault('editable', False)
            kwargs['blank'] = True

        if version == 1:
            self.node, self.clock_seq = node, clock_seq
        elif version in (3, 5):
            self.namespace, self.name = namespace, name

        super(UUIDField, self).__init__(verbose_name, name, **kwargs)

    def get_internal_type (self):
        return CharField.__name__

    def generate_uuid (self):
        if not self.version or self.version == 4:
            return uuid.uuid4()
        elif self.version == 1:
            return uuid.uuid1(self.node, self.clock_seq)
        elif self.version == 3:
            return uuid.uuid3(self.namespace, self.name)
        elif self.version == 5:
            return uuid.uuid5(self.namespace, self.name)
        else:
            # We shouldn't ever get to this point, but just in case
            raise UUIDVersionError("UUID version %s is not valid." % self.version)

    def pre_save (self, model_instance, add):
        value = super(UUIDField, self).pre_save(model_instance, add)

        if self.auto_update or (self.auto and (add or not value)):
            value = unicode(self.generate_uuid())
            setattr(model_instance, self.attname, value)

        return value
