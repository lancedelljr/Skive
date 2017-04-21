from django.conf.urls import url
from . import views

app_name = 'Teacher'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^info/$', views.info, name='info'),
    url(r'^visitor_info/$', views.visitor_info, name='visitor_info'),
    url(r'^create_account/$', views.create_account, name='create_account'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^(?P<course_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^create_course/$', views.create_course, name='create_course'),
    url(r'^(?P<course_id>[0-9]+)/delete_course/$', views.delete_course, name='delete_course'),
    url(r'^(?P<course_id>[0-9]+)/create_student/$', views.create_student, name='create_student'),
    url(r'^(?P<course_id>[0-9]+)/add_absence/(?P<student_id>[0-9]+)/$', views.add_absence, name='add_absence'),
    url(r'^(?P<course_id>[0-9]+)/subtract_absence/(?P<student_id>[0-9]+)/$', views.sub_absence, name='sub_absence'),
    url(r'^(?P<course_id>[0-9]+)/delete_student/(?P<student_id>[0-9]+)/$', views.delete_student, name='delete_student'),
]
