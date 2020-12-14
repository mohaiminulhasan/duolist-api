from django.contrib import admin
from .models import List, ListItem, Profile, Notification, Invite
# Register your models here.
admin.site.register(List)
admin.site.register(ListItem)
admin.site.register(Profile)
admin.site.register(Notification)
admin.site.register(Invite)
