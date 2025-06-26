from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .models import StudentProfile, Assignment, Course, Enrollment
from .forms import CourseForm
from .forms import CustomRegistrationForm
from .models import StudentProfile, InstructorProfile


# Custom login view
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

# Home page view    
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from core.models import InstructorProfile, StudentProfile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')  # Match this with the form field name
        confirm_password = request.POST.get('password2')  # Match this with the form field name

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Your account has been successfully created.")
        login(request, user)  # Log the user in after registration
        return redirect('home')

    return render(request, 'registration/register.html')



@login_required
def home(request):
    courses = Course.objects.all()  # Fetch all courses from the database
    return render(request, 'core/home.html', {'courses': courses})

    if not request.user.is_authenticated:  # If user is not logged in
        return redirect('login')  # Redirect to login page
    
    # Debugging
    print("Is Instructor:", hasattr(request.user, 'instructorprofile'))
    print("Is Student:", hasattr(request.user, 'studentprofile'))

    # Check user roles and redirect
    if hasattr(request.user, 'instructorprofile') and request.user.instructorprofile:
        return redirect('instructor_courses')
    elif hasattr(request.user, 'studentprofile') and request.user.studentprofile:
        return redirect('course_list')
    else:
        return render(request, 'core/home.html')


# View to list all courses
# @login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'core/course_list.html', {'courses': courses})

# View to display course details along with assignments
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    assignments = Assignment.objects.filter(course=course)
    return render(request, 'core/course_detail.html', {
        'course': course,
        'assignments': assignments,
    })

# View for enrolling in a course
@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user not in course.students.all():
        course.students.add(request.user)
        messages.success(request, "You have successfully enrolled in the course!")
    else:
        messages.info(request, "You are already enrolled in this course.")
    return redirect('course_detail', course_id=course.id)

# View for unenrolling from a course
@login_required
def unenroll_from_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user in course.students.all():
        course.students.remove(request.user)
        messages.success(request, "You have successfully unenrolled from the course.")
    else:
        messages.info(request, "You are not enrolled in this course.")
    return redirect('course_detail', course_id=course.id)

# Registration view for new users
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages

 
# Login view
def login_view(request):
    if request.method == "POST": 
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Logout view
def logout_view(request):
    auth_logout(request)
    return redirect('login')

# View for uploading an assignment
@login_required
def upload_assignment(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        assignment_id = request.POST.get('assignment')
        uploaded_file = request.FILES.get('file')
        assignment = get_object_or_404(Assignment, id=assignment_id, course=course)
        assignment.submitted_file = uploaded_file
        assignment.student = request.user
        assignment.save()
        messages.success(request, "Assignment submitted successfully!")
        return redirect('course_detail', course_id=course_id)
    messages.error(request, "Failed to submit the assignment.")
    return redirect('course_detail', course_id=course_id)
# View for grading an assignment
@login_required
def grade_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == "POST":
        grade = request.POST.get("grade")
        assignment.grade = grade
        assignment.save()
        return redirect('course_detail', course_id=assignment.course.id)
    return render(request, 'core/grade_assignment.html', {'assignment': assignment})

# Instructor's courses view
@login_required
def instructor_courses(request):
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'core/instructor_courses.html', {'courses': courses})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user.instructorprofile)
    course.delete()
    messages.success(request, "Course deleted successfully.")
    return redirect('instructor_courses')


# View for creating a course
@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('instructor_courses')
    else:
        form = CourseForm()
    return render(request, 'core/create_course.html', {'form': form})
