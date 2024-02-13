from django.contrib.auth import get_user_model
from django.db import models
from qux.models import QuxModel


class Faculty(QuxModel):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    github = models.CharField(max_length=39, unique=True)
    is_active = models.BooleanField(default=True)

    def programs(self):
        return Program.objects.none()

    def courses(self):
        return Course.objects.none()

    def content(self, program=None, course=None):
        return Course.objects.none()

    def assignments_graded(self, assignment=None):
        return StudentAssignment.objects.none()


class Program(QuxModel):
    """
    Example: Cohort-2
    """

    name = models.CharField(max_length=128)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.name

    def students(self):
        """
        List of students in the program
        """
        return Student.objects.none()


class Course(QuxModel):
    """
    Example: Python, or Django, or Logic
    """

    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    def programs(self):
        return Program.objects.none()

    def students(self):
        return Student.objects.none()

    def content(self):
        return Content.objects.none()

    def assignments(self):
        return Assignment.objects.none()


class Content(QuxModel):
    """
    Meta information related to a GitHub repo
    """

    name = models.CharField(max_length=128)
    faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING)
    repo = models.URLField(max_length=240, unique=True)

    class _Meta:
        verbose_name = "Content"
        verbose_name_plural = "Content"


class Student(QuxModel):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    github = models.CharField(max_length=39, unique=True)
    is_active = models.BooleanField(default=True)
    program = models.ForeignKey(Program, on_delete=models.DO_NOTHING)

    def courses(self):
        return Course.objects.none()

    def assignments(self):
        return Assignment.objects.none()

    def assignments_submitted(self, assignment=None):
        return StudentAssignment.objects.none()

    def assignments_not_submited(self, assignment=None):
        return StudentAssignment.objects.none()

    def assignments_graded(self, assignment=None):
        return StudentAssignment.objects.none()


class Assignment(QuxModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    due = models.DateTimeField()
    instructions = models.TextField()
    rubric = models.TextField()

    class Meta:
        unique_together = ["program", "course", "content"]

    def __str__(self):
        return self.content.name

    def students(self):
        return Student.objects.none()

    def submissions(self, graded=None):
        """
        Return a queryset of submissions that are either all, graded, or not graded.
        """
        return StudentAssignment.objects.none()


class StudentAssignment(QuxModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=None,
        null=True,
        blank=True,
    )
    submitted = models.DateTimeField(default=None, null=True, blank=True)
    reviewed = models.DateTimeField(default=None, null=True, blank=True)
    reviewer = models.ForeignKey(
        Faculty, on_delete=models.DO_NOTHING, default=None, null=True, blank=True
    )
    feedback = models.TextField(default=None, null=True, blank=True)
