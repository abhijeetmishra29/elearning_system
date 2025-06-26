from django.contrib import admin
from .models import Course, Assignment, StudentProfile
from .models import InstructorProfile
from .models import Material


# Register your models here.
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(StudentProfile)
admin.site.register(InstructorProfile)
admin.site.register(Material)