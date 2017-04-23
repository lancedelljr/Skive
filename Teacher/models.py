from django.db import models
from django.contrib.auth.models import Permission, User


class Course(models.Model):
    user = models.ForeignKey(User, default=1)
    department = models.CharField(max_length=3)
    course_number = models.CharField(max_length=3)
    section = models.IntegerField(default=1)
    title = models.CharField(max_length=100)
    semester = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    days = models.CharField(max_length=25)
    time = models.CharField(max_length=25)

    def __str__(self):
        return self.department + '-' + self.course_number + '-' + str(self.section) + ' ' + self.title + \
               ' - ' + self.semester + ' ' + self.year + ' ' + self.days + ' ' + self.time


class Student(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, default='username@example.com')
    absences = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.student_name
