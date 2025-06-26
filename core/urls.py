from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import View

# Custom logout view to allow GET requests
class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')  # Redirect to login page after logout

# Core app URLs
urlpatterns = [
    # General
    path('', views.home, name='home'),  # Root path redirects to the home view
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Default template: registration/login.html
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Student Views
    path('courses/', views.course_list, name='course_list'),  # List of all courses
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),  # Course details with assignments
    path('enroll/<int:course_id>/', views.enroll_in_course, name='enroll_in_course'),  # Enroll in a course
    path('unenroll/<int:course_id>/', views.unenroll_from_course, name='unenroll_from_course'),  # Unenroll from a course
    path('course/<int:course_id>/upload_assignment/', views.upload_assignment, name='upload_assignment'),  # Upload an assignment

    # Instructor Views
    path('instructor/courses/', views.instructor_courses, name='instructor_courses'),  # Instructor's course list
    path('course/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('create_course/', views.create_course, name='create_course'),  # Create a new course
    path('grade_assignment/<int:assignment_id>/', views.grade_assignment, name='grade_assignment'),  # Grade an assignment
]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
