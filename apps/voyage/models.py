"""
database tables  for voyage app
"""

import random
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.db import models
from qux.models import QuxModel


class Faculty(QuxModel):
    """
    Represents a faculty member.
    """

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    github = models.CharField(max_length=39, unique=True)
    is_active = models.BooleanField(default=True)

    @classmethod
    def create_random_faculty(cls):
        """
        Creates and saves random faculty members.
        """
        for i in range(1, 6):
            user = get_user_model().objects.create_user(
                username=f"faculty_{i}",
                email=f"e9{i}@gmail.com",
                password="password{i}",
            )
            faculty = cls(
                user=user,
                github=f"github_{random.randint(1000, 9999)}",
                is_active=random.choice([True, False]),
            )
            faculty.save()

        return faculty

    def programs(self):
        """
        Returns a list of programs associated with the faculty.
        """

        student_assignments = self.studentassignment_set.all()
        prog = set()

        for assignment in student_assignments:
            prog.add(assignment.student.program)

        return list(prog)

    def courses(self):
        """
        Returns a list of courses associated with the faculty.
        """

        contents = self.content_set.all()
        con = set()
        for content in contents:
            assigments = content.assignment_set.all()
            for assigment in assigments:
                con.add(assigment.course)

        return list(con)

    def content(self, program=None, course=None):
        """
        Returns content based on the provided program and/or course.
        """

        content_list = self.content_set.all()
        if program and course:
            for i in content_list:
                return i.assignment_set.filter(program=program, course=course)
        elif program:
            for i in content_list:
                return i.assignment_set.filter(program=program)
        elif course:
            for i in content_list:
                return i.assignment_set.filter(course=course)
        else:
            for i in content_list:
                return i.assignment_set.all()

    def assignments_graded(self, assignment=None):
        """
        Returns a list of graded assignments associated with the faculty.
        """
        graded_assignments = set()

        if assignment:
            graded_assignments = self.studentassignment_set.filter(
                assignment=assignment, grade__isnull=False
            )
        else:
            graded_assignments = self.studentassignment_set.filter(grade__isnull=False)

        return list(graded_assignments)

    def num_assignments(self):
        """
        Returns a list of all assignments associated with the faculty.
        """

        a = []
        assignmnets = self.studentassignment_set.all()
        for assignment in assignmnets:
            a.append(assignment)
        return a


class Program(QuxModel):
    """
    Represents an educational program.
    """

    name = models.CharField(max_length=128)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.name

    def students(self):
        """
        Returns students.
        """
        return self.student_set.all()

    @classmethod
    def create_random_program(cls):
        """
        Creates and saves random programs.
        """
        for i in range(1, 4):
            program = cls(
                name=f"Program_{i}",
                start=datetime.now() - timedelta(days=random.randint(30, 365)),
                end=datetime.now() + timedelta(days=random.randint(30, 365)),
            )
            program.save()

        return program


class Course(QuxModel):
    """
    Represents a course.
    """

    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    def programs(self):
        """
        Returns a set of programs associated with the course.
        """
        return {assignment.program for assignment in self.assignment_set.all()}

    def students(self):
        """
        Returns a set of students associated with the course.
        """
        stu = set()
        for assignment in self.assignment_set.all():
            for s in assignment.studentassignment_set.all():
                stu.add(s.student)
        return stu

    def content(self):
        """
        Returns a set of content associated with the course.
        """
        return {assignment.content for assignment in self.assignment_set.all()}

    def assignments(self):
        """
        Returns a set of assignments associated with the course.
        """
        return set(self.assignment_set.all())

    @classmethod
    def create_random_course(cls):
        """
        Creates and saves random courses.
        """
        for i in range(1, 4):
            course = cls(name=f"Course_{i}")
            course.save()

        return course


class Content(QuxModel):
    """
    Represents educational content.
    """

    name = models.CharField(max_length=128)
    faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING)
    repo = models.URLField(max_length=240, unique=True)

    class Meta:
        verbose_name = "Content"
        verbose_name_plural = "Content"

    @classmethod
    def create_random_content(cls):
        """
        created random data for Content model
        """
        faculties = Faculty.objects.all()
        for i in range(1, 29):
            faculty = random.choice(faculties)

            content = cls(
                name=f"Content_{i}",
                faculty=faculty,
                repo=f"https://github.com/{faculty.github}/repo_{i}",
            )
            content.save()

        return content


class Student(QuxModel):
    """
    Represents a student enrolled in a specific program.
    """

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    github = models.CharField(max_length=39, unique=True)
    is_active = models.BooleanField(default=True)
    program = models.ForeignKey(Program, on_delete=models.DO_NOTHING)

    def courses(self):
        """
        Returns a set of courses associated with the student's program.
        """

        c = set()

        for a in self.program.assignment_set.all():
            c.add(a.course)
        return c

    def assignments(self):
        """
        Returns all assignments associated with the student's program.
        """
        return self.program.assignment_set.all()

    def assignments_submitted(self, assignment=None):
        """
        Returns a set of submitted assignments, optionally filtered by assignment.
        """

        if assignment:
            return self.studentassignment_set.filter(
                assignment=assignment, submitted__isnull=False
            )
        return self.studentassignment_set.filter(submitted__isnull=False)

    def assignments_not_submited(self, assignment=None):
        """
        Returns assignments that have not been submitted, optionally filtered by assignment.
        """

        if assignment:
            return self.studentassignment_set.filter(
                assignment=assignment, submitted__isnull=True
            )
        return self.studentassignment_set.filter(submitted__isnull=True)

    def assignments_graded(self, assignment=None):
        """
        Returns graded assignments, optionally filtered by assignment.
        """

        if assignment:
            return self.studentassignment_set.filter(
                assignment=assignment, submitted__isnull=False, grade__isnull=False
            )
        return self.studentassignment_set.filter(
            submitted__isnull=False, grade__isnull=False
        )

    @classmethod
    def create_random_student(cls):
        """
        Creates and saves random students with associated programs.
        """

        programs = Program.objects.all()
        for i in range(1, 11):
            user = get_user_model().objects.create_user(
                username=f"student_{random.randint(1000, 9999)}",
                email=f"e9student{i}@gmail.com",
                password="password{i}",
            )
            program = random.choice(programs)
            student = cls(
                user=user,
                github=f"github_{random.randint(1000, 9999)}",
                is_active=random.choice([True, False]),
                program=program,
            )
            student.save()
        return student


class Assignment(QuxModel):
    """
    Represents an assignment given to students in a specific program and course.
    """

    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    due = models.DateTimeField()
    instructions = models.TextField()
    rubric = models.TextField()

    class Meta:
        unique_together = ["program", "course", "content"]

    def __str__(self):
        """
        Returns a string representation of the assignment.
        """
        return self.content.name

    def students(self):
        """
        Returns a set of students who have been assigned this assignment.
        """

        students_set = set()

        student_assignments = self.studentassignment_set.all()

        for s_assignment in student_assignments:
            student = s_assignment.student

            if student:
                students_set.add(student)
        return students_set

    def submissions(self, graded=None):
        """
        Return a queryset of submissions that are either all, graded, or not graded.
        """
        submissions_query = self.studentassignment_set.all()

        if graded is not None:
            if graded:
                submissions_query = submissions_query.filter(grade__isnull=False)
            else:
                submissions_query = submissions_query.filter(grade__isnull=True)

        return submissions_query

    @classmethod
    def create_random_assignment(cls):
        """
        Creates and saves random assignments with associated programs, courses, and content.
        """

        programs = Program.objects.all()
        courses = Course.objects.all()
        contents = Content.objects.all()

        for _ in range(1, 6):
            program = random.choice(programs)
            course = random.choice(courses)
            content = random.choice(contents)
            due_date = datetime.now() + timedelta(days=random.randint(7, 30))

            assignment = cls(
                program=program,
                course=course,
                content=content,
                due=due_date,
                instructions=f"Instructions for Assignment_{random.randint(100, 999)}",
                rubric=f"Rubric for Assignment_{random.randint(100, 999)}",
            )
            assignment.save()

        return assignment


class StudentAssignment(QuxModel):
    """
    Represents an assignment submitted by a student, along with grading details.
    """

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

    @classmethod
    def create_random_student_assignment(cls):
        """
        Creates and saves random student assignments with
        associated students, assignments, and faculties.
        """

        students = Student.objects.all()
        assignments = Assignment.objects.all()
        faculties = Faculty.objects.all()
        for _ in range(1, 11):
            student = random.choice(students)
            assignment = random.choice(assignments)
            faculty = random.choice(faculties)

            submitted_date = datetime.now() - timedelta(days=random.randint(0, 7))
            reviewed_date = submitted_date + timedelta(days=random.randint(0, 7))

            student_assignment = cls(
                student=student,
                assignment=assignment,
                grade=random.choice([None, random.uniform(60, 100)]),
                submitted=submitted_date,
                reviewed=reviewed_date,
                reviewer=faculty,
                feedback=f"Feedback for Assignment_{assignment.id}",
            )
            student_assignment.save()

        return student_assignment
