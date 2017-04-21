from django.contrib import admin
from .models import Course, Student, UserProfile

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(UserProfile)
