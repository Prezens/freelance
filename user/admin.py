from django.contrib import admin
from .models import User, LogTransaction

admin.site.register(User)
admin.site.register(LogTransaction)
