from django.contrib import admin
from .models import User, Feeds
# Register your models here.

admin.site.register([User, Feeds])