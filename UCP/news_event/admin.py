from django.contrib import admin
from news_event.models import News, Event

# Register your models here.
admin.site.register(News)
admin.site.register(Event)