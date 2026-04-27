from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view),
    path('attendance/', views.attendance_view),
    path('marks/', views.marks_view),
    path('assignments/', views.assignment_view),
    path('submit/<int:id>/', views.submit_assignment),
    path('faculty/', views.faculty_dashboard),
    path('mark-attendance/', views.mark_attendance),
    path('add-assignment/', views.add_assignment),
    path('add-marks/', views.add_marks),
    path('notifications/', views.notifications_view),
    path('add-notification/', views.add_notification),
]