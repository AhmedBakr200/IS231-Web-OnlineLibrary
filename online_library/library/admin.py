from django.contrib import admin
from .models import Book, BorrowRecord, Profile

admin.site.register(Book)
admin.site.register(BorrowRecord)
admin.site.register(Profile)