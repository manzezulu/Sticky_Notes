# notes/admin.py
from django.contrib import admin

from .models import Note

# Register your models here.
admin.site.register(Note)
