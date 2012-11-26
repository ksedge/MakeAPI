from django.db import models
from MakeAPI.db.fields import UUIDField


class Make (models.Model):

    id = UUIDField(version=4, primary_key=True, verbose_name='ID')
    version = UUIDField(version=4, auto_update=True)
    url = models.URLField(verbose_name='URL')
    content_type = models.CharField(max_length=255, verbose_name='Content Type')
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __unicode__ (self):
        return self.id

    @property
    def published (self):
        return self.published_at is not None

    @property
    def deleted (self):
        return self.deleted_at is not None

    @models.permalink
    def get_absolute_url (self):
        return ('makes_resource', (), {
            'id': self.id,
        })
