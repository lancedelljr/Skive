# url patterns for the Teacher app

from django.conf.urls import url
from . import views

app_name = 'Teacher'

urlpatterns = [
    
    # skivetracker.herokuapp.com/courses
    url(r'^courses/$', views.index, name='index'),
    
    # skivetracker.herokuapp.com/info
    url(r'^info/$', views.info, name='info'),
    
    # skivetracker.herokuapp.com/visitor_info
    url(r'^visitor_info/$', views.visitor_info, name='visitor_info'),
    
    # skivetracker.herokuapp.com/create_account
    url(r'^create_account/$', views.create_account, name='create_account'),

    # skivetracker.herokuapp.com/login
    url(r'^login/$', views.user_login, name='user_login'),

    # skivetracker.herokuapp.com/logout
    url(r'^logout/$', views.user_logout, name='user_logout'),

    # skivetracker.herokuapp.com/profile
    url(r'^profile/$', views.profile, name='profile'),
 
    # skivetracker.herokuapp.com/change_password
    url(r'^change_password/$', views.change_password, name='change_password'),
 
    # skivetracker.herokuapp.com/4
    url(r'^(?P<course_id>[0-9]+)/$', views.detail, name='detail'),
 
    # skivetracker.herokuapp.com/create_course
    url(r'^create_course/$', views.create_course, name='create_course'),

    # skivetracker.herokuapp.com/4/delete_course
    url(r'^(?P<course_id>[0-9]+)/delete_course/$', views.delete_course, name='delete_course'),

    # skivetracker.herokuapp.com/4/create_student
    url(r'^(?P<course_id>[0-9]+)/create_student/$', views.create_student, name='create_student'),

    # skivetracker.herokuapp.com/4/add_absence/2
    url(r'^(?P<course_id>[0-9]+)/add_absence/(?P<student_id>[0-9]+)/$', views.add_absence, name='add_absence'),

    # skivetracker.herokuapp.com/4/subtract_absence/2
    url(r'^(?P<course_id>[0-9]+)/subtract_absence/(?P<student_id>[0-9]+)/$', views.sub_absence, name='sub_absence'),
 
    # skivetracker.herokuapp.com/4/delete_student/2
    url(r'^(?P<course_id>[0-9]+)/delete_student/(?P<student_id>[0-9]+)/$', views.delete_student, name='delete_student'),
]
