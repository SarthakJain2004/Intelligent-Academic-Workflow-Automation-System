from django.contrib import admin
from .models import Student, Attendance, Assignment, Marks,Subject

admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Assignment)
admin.site.register(Marks)
admin.site.register(Subject)

# Register your models here.
