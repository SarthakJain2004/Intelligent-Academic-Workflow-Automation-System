from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Subject
from .models import Attendance, Marks, Assignment, Submission, Student
from django.utils import timezone
from .models import Notification
from django.contrib.auth.decorators import login_required
from datetime import timedelta

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # ROLE CHECK
            if role == "faculty" and user.groups.filter(name='Faculty').exists():
                return redirect('/faculty/')

            elif role == "student" and user.groups.filter(name='Student').exists():
                return redirect('/dashboard/')

            else:
                return render(request, 'login.html', {
                    'error': 'Invalid role selected'
                })

        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'login.html')   # 🔥 IMPORTANT


def logout_view(request):
    logout(request)
    return redirect('/')


def attendance_view(request):
    student = Student.objects.get(user=request.user)
    subjects = Subject.objects.all()

    selected_subject = request.GET.get('subject')

    attendance_data = []
    percentage = 0

    if selected_subject:
        data = Attendance.objects.filter(
            student=student,
            subject_id=selected_subject
        ).order_by('-date')

        total = data.count()
        present = data.filter(status=True).count()

        percentage = (present / total * 100) if total > 0 else 0

        attendance_data = data

    return render(request, 'attendance.html', {
        'subjects': subjects,
        'attendance_data': attendance_data,
        'percentage': percentage
    })


import json

def marks_view(request):
    student = Student.objects.get(user=request.user)
    data = Marks.objects.filter(student=student)

    total = sum(i.marks for i in data)
    count = data.count()
    percentage = (total / (count * 100)) * 100 if count > 0 else 0

    labels = [str(i.subject) for i in data]
    marks = [i.marks for i in data]

    return render(request, 'marks.html', {
        'data': data,
        'total': total,
        'percentage': round(percentage, 2),
        'labels': json.dumps(labels),
        'marks_list': json.dumps(marks)
    })


def assignment_view(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignments.html', {'assignments': assignments})


def submit_assignment(request, id):
    if request.method == "POST":
        student = Student.objects.get(user=request.user)
        assignment = Assignment.objects.get(id=id)

        Submission.objects.create(
            student=student,
            assignment=assignment,
            file=request.FILES['file']
        )

        return redirect('/assignments/')


@login_required
def faculty_dashboard(request):
    if not request.user.groups.filter(name='Faculty').exists():
        return redirect('/')

    return render(request, 'faculty_dashboard.html')

def mark_attendance(request):
    students = Student.objects.all()
    subjects = Subject.objects.all()

    if request.method == "POST":
        student = Student.objects.get(id=request.POST['student'])
        subject = Subject.objects.get(id=request.POST['subject'])
        status = request.POST['status'] == "present"

        Attendance.objects.create(
            student=student,
            subject=subject,
            status=status
        )

    return render(request, 'mark_attendance.html', {
        'students': students,
        'subjects': subjects
    })

def add_assignment(request):
    subjects = Subject.objects.all()

    if request.method == "POST":
        Assignment.objects.create(
            title=request.POST['title'],
            subject_id=request.POST['subject'],
            deadline=request.POST['deadline']
        )

    return render(request, 'add_assignment.html', {'subjects': subjects})

def add_marks(request):
    students = Student.objects.all()
    subjects = Subject.objects.all()

    if request.method == "POST":
        Marks.objects.create(
            student_id=request.POST['student'],
            subject_id=request.POST['subject'],
            marks=request.POST['marks']
        )

    return render(request, 'add_marks.html', {
        'students': students,
        'subjects': subjects
    })


from datetime import datetime

def dashboard(request):
    # delete old notifications
    Notification.objects.filter(
        created_at__lt=timezone.now() - timedelta(days=2)
    ).delete()

    last_seen = request.session.get('last_seen')

    if last_seen:
        last_seen = datetime.fromisoformat(last_seen)  # 🔥 FIX
        count = Notification.objects.filter(created_at__gt=last_seen).count()
    else:
        count = Notification.objects.count()

    return render(request, 'dashboard.html', {
        'count': count
    })

def notifications_view(request):
    data = Notification.objects.all().order_by('-created_at')

    # ✅ store proper datetime
    request.session['last_seen'] = timezone.now().isoformat()

    return render(request, 'notifications.html', {
        'data': data
    })

def add_notification(request):
    if request.method == "POST":
        Notification.objects.create(
            title=request.POST['title'],
            message=request.POST['message']
        )
        return redirect('/faculty/')  # optional redirect

    return render(request, 'add_notification.html')

# Create your views here.
