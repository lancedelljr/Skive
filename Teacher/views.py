from django.conf import settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from .forms import UserForm, CourseForm, StudentForm
from .models import Course, Student


# returns visitor_info.html for unauthenticated users
def visitor_info(request):
    return render(request, 'Teacher/visitor_info.html')


# returns info.html for authenticated users
def info(request):
    return render(request, 'Teacher/info.html')


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'Teacher/visitor_info.html')
    else:
        courses = Course.objects.filter(user=request.user)
    return render(request, 'Teacher/index.html', {'courses': courses})


def detail(request, course_id):
    if not request.user.is_authenticated():
        return render(request, 'Teacher/visitor_info.html')
    else:
        user = request.user
        course = get_object_or_404(Course, pk=course_id)
    return render(request, 'Teacher/detail.html', {'course': course, 'user': user})


def create_course(request):
    if not request.user.is_authenticated():
        return render(request, 'Teacher/visitor_info.html')
    else:
        form = CourseForm(request.POST or None)
        if form.is_valid():
            all_courses = Course.objects.all()
            for c in all_courses:
                if c.department == form.cleaned_data.get("department"):
                    if c.course_number == form.cleaned_data.get("course_number"):
                        if c.section == form.cleaned_data.get("section"):
                            context = {
                                'form': form,
                                'error_message': 'This course has already been created'
                            }
                            return render(request, 'Teacher/create_course.html', context)
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            return render(request, 'Teacher/detail.html', {'course': course})
    return render(request, 'Teacher/create_course.html', {'form': form})


def create_student(request, course_id):
    form = StudentForm(request.POST or None)
    course = get_object_or_404(Course, pk=course_id)
    if form.is_valid():
        courses_students = course.student_set.all()
        for s in courses_students:
            if s.student_name == form.cleaned_data.get("student_name"):
                context = {
                    'course': course,
                    'form': form,
                    'error_message': 'This student has already been added',
                }
                return render(request, 'Teacher/create_student.html', context)
        student = form.save(commit=False)
        student.course = course
        student.save()

        # send email confirmation email to student when they are added to the course
        subject = 'Skive: Attendance Tracker'
        message = 'Welcome ' + student.student_name + '!' + \
            '\n\nYour professor has added you to ' + course.department + '-' + course.course_number + \
            '-' + str(course.section) + ' ' + course.title + '.' + \
            ' Now you will be notified each time an absence is added.\n\nSkive'
        from_email = settings.EMAIL_HOST_USER
        to_list = [student.email, settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return render(request, 'Teacher/detail.html', {'course': course})
    context = {
        'course': course,
        'form': form,
    }
    return render(request, 'Teacher/create_student.html', context)


def delete_course(request, course_id):
    course = Course.objects.get(pk=course_id)
    course.delete()
    courses = Course.objects.filter(user=request.user)
    context = {
        'courses': courses,
        'delete_message': course.department + '-' + course.course_number + '-' + str(course.section) +
        ' ' + course.title + ' ' + 'has been deleted',
    }
    return render(request, 'Teacher/index.html', context)


def delete_student(request, course_id, student_id):
    course = get_object_or_404(Course, pk=course_id)
    student = Student.objects.get(pk=student_id)
    student.delete()
    context = {
        'course': course,
        'delete_message': student.student_name + ' ' + 'has been deleted'
    }
    return render(request, 'Teacher/detail.html', context)


def add_absence(request, course_id, student_id):
    course = get_object_or_404(Course, pk=course_id)
    student = Student.objects.get(pk=student_id)
    student.absences += 1
    student.save()

    # send student email to see total absences
    subject = course.department + '-' + course.course_number + \
        '-' + str(course.section) + ' ' + course.title + ' Absence Update'
    message = student.student_name + ',' + \
        '\n\nYour absences have been updated for ' + course.department + '-' + course.course_number + \
        '-' + str(course.section) + ' ' + course.title + '.' + \
        '\n\nTotal absences = ' + str(student.absences) + '\n\nSkive'
    from_email = settings.EMAIL_HOST_USER
    to_list = [student.email, settings.EMAIL_HOST_USER]
    send_mail(subject, message, from_email, to_list, fail_silently=True)

    return render(request, 'Teacher/detail.html', {'course': course})


def sub_absence(request, course_id, student_id):
    course = get_object_or_404(Course, pk=course_id)
    student = Student.objects.get(pk=student_id)
    if student.absences == 0:
        context = {
            'course': course,
            'error_message': 'Absences cannot be negative'
        }
        return render(request, 'Teacher/detail.html', context)
    student.absences -= 1
    student.save()
    return render(request, 'Teacher/detail.html', {'course': course})


def create_account(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()

        # send confirmation email
        subject = 'Skive: Attendance Tracker'
        message = 'Welcome ' + user.first_name + '!' + \
            '\n\nNow you can start creating courses, adding students, and editing absences.\n\nSkive'
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email, settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                courses = Course.objects.filter(user=request.user)
                return render(request, 'Teacher/index.html', {'courses': courses})
    return render(request, 'Teacher/create_account.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                courses = Course.objects.filter(user=request.user)
                return render(request, 'Teacher/index.html', {'courses': courses})
            else:
                return render(request, 'Teacher/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'Teacher/login.html', {'error_message': 'Invalid login'})
    return render(request, 'Teacher/login.html')


def user_logout(request):
    logout(request)
    return render(request, 'Teacher/visitor_info.html')


def profile(request):
    if not request.user.is_authenticated():
        return render(request, 'Teacher/visitor_info.html')
    else:
        courses = Course.objects.filter(user=request.user)
        courses_count = courses.count()
        return render(request, 'Teacher/profile.html', {'courses_count': courses_count})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            context = {
                'form': form,
                'error_message': 'Password changed'
            }
            return render(request, 'Teacher/change_password.html', context)
        else:
            context = {
                'form': form,
                'error_message': 'Please correct the error'
            }
            return render(request, 'Teacher/change_password.html', context)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Teacher/change_password.html', {'form': form})
