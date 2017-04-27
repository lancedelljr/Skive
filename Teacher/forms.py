# forms based on the models

from django.contrib.auth.models import User
from django import forms
from .models import Course, Student


# user form based on the user model for authentication
class UserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


# course form based on the course model for adding courses
class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['department', 'course_number', 'section', 'title', 'semester', 'year', 'days', 'time']


# student form based on the student model for adding students
class StudentForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput)

    class Meta:
        model = Student
        fields = ['student_name', 'email', 'absences']
