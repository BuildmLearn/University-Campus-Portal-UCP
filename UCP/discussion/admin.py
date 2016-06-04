from django.contrib import admin

from discussion.models import DiscussionThread, Reply, Attachment
# Register your models here.

admin.site.register(DiscussionThread)
admin.site.register(Reply)
admin.site.register(Attachment)