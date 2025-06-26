from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructorprofile')
    # You can add additional fields here if needed
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='instructors/', blank=True, null=True)

    def __str__(self):
        return f"Instructor Profile for {self.user.username}"
    
    
# Model to represent a Course
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='courses', blank=True)
    # other fields like duration, date, etc.

    def __str__(self):
        return self.title

# Model to represent an Assignment for a Course
class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    course = models.ForeignKey(Course, related_name='assignments', on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    submitted_file = models.FileField(upload_to='assignment_submissions/', null=True, blank=True)
    grade = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.title

# Model to represent an Enrollment of a Student in a Course
class Enrollment(models.Model):
    student = models.ForeignKey(User, related_name="enrollments", on_delete=models.CASCADE)  # Linking to the User model
    course = models.ForeignKey(Course, related_name="enrollments", on_delete=models.CASCADE)  # Linking to the Course model
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')  # Ensures a student can't enroll in the same course more than once

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"

# You can use Django's built-in User model, or extend it for custom attributes like role, etc.
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # This is optional; you can link StudentProfile to a Course through the Enrollment model instead
    # course = models.ForeignKey(Course, related_name="students", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} Profile"

class Material(models.Model):
    course = models.ForeignKey('Course', related_name='materials', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='materials/')

    def __str__(self):
        return self.title