from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Comment, CustomUser, Genre, Review, Title

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comment)
