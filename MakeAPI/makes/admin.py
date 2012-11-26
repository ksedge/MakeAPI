from MakeAPI.makes.models import Make
from django.contrib import admin


class MakeAdmin(admin.ModelAdmin):
    readonly_fields = ('id','version','created_at','published_at','updated_at',)
    list_display = ('id', 'created_at', 'content_type', )
    list_filter = ('content_type', 'created_at', 'updated_at',)


admin.site.register(Make, MakeAdmin)
