from django.contrib.auth.models import User
from django import forms
from .models import Course, Student


class UserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['department', 'course_number', 'section', 'title', 'semester', 'year', 'days', 'time']


class StudentForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput)

    class Meta:
        model = Student
        fields = ['student_name', 'email', 'absences']
