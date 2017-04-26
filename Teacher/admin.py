# allows Courses and Students to be viewed and manipulated from the admin page

from django.contrib import admin
from .models import Course, Student

admin.site.register(Course)
admin.site.register(Student)
