from django.contrib.auth.models import User
from django import forms
from .models import Course, Student, Profile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs['instance'].user
        user_kwargs = kwargs.copy()
        user_kwargs['instance'] = self.user
        self.uf = UserForm(*args, **user_kwargs)

        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields.update(self.uf.fields)
        self.initial.update(self.uf.initial)

    def save(self, *args, **kwargs):
        # save both forms
        self.uf.save(*args, **kwargs)
        return super(ProfileForm, self).save(*args, **kwargs)

    class Meta:
        model = Profile
        fields = ['account_type']


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['department', 'course_number', 'section', 'title', 'semester', 'year', 'days', 'time']


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['student_name', 'absences']
