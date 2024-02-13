from django.contrib import admin
from django.db.models import Avg
from django.contrib import admin
from django.db.models import Count
from .models import (
    Faculty,
    Content,
    Program,
    Course,
    Student,
    Assignment,
    StudentAssignment,
)

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('user', 'github', 'is_active', 'num_courses_taught', 'num_assignments_graded')

    def num_courses_taught(self, obj):
        return len(obj.programs())

    def num_assignments(self, obj):
        return obj.assignments.count()

    def num_assignments_graded(self, obj):
        return StudentAssignment.objects.filter(reviewer=obj, grade__isnull=False).count()

    num_courses_taught.short_description = 'Number of Courses Taught'
    num_assignments.short_description = 'Number of Assignments'
    num_assignments_graded.short_description = 'Number of Assignments Graded'




@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'github', 'is_active', 'program_name', 'num_courses_enrolled', 'num_assignments', 'average_grade')

    def program_name(self, obj):
        return obj.program.name

    def num_courses_enrolled(self, obj):
        return len(obj.courses())

    def num_assignments(self, obj):
        return obj.assignments().count()

    def num_assignments_submitted(self, obj):
        return len(obj.assignments_submitted())






    def average_grade(self, obj):
        submitted_assignments = obj.studentassignment_set.filter(grade__isnull=False)
        if submitted_assignments.exists():
            return submitted_assignments.aggregate(Avg('grade'))['grade__avg']
        return None

    program_name.short_description = 'Program Enrolled In'
    num_courses_enrolled.short_description = 'Number of Courses Enrolled In'
    num_assignments.short_description = 'Number of Assignments Assigned'
    num_assignments_submitted.short_description = 'Number of Assignments Submitted'
    average_grade.short_description = 'Average Grade'

    list_filter = ('program',) 


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty', 'repo', 'num_courses', 'num_assignments')

    def num_courses(self, obj):
        return obj.assignment_set.values('course').annotate(course_count=Count('course')).count()

    def num_assignments(self, obj):
        return obj.assignment_set.count()

    num_courses.short_description = 'Number of Courses'
    num_assignments.short_description = 'Number of Assignments'



@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'num_courses', 'num_students')

    def num_courses(self, obj):
        return obj.assignment_set.values('course').annotate(course_count=Count('course')).count()

    def num_students(self, obj):
        return obj.student_set.count()

    num_courses.short_description = 'Number of Courses'
    num_students.short_description = 'Number of Students'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'num_assignments', 'num_completed_assignments')

    def num_assignments(self, obj):
        return obj.assignment_set.count()

    def num_completed_assignments(self, obj):
        return obj.assignment_set.filter(studentassignment__grade=100).count()

    num_assignments.short_description = 'Number of Assignments'
    num_completed_assignments.short_description = 'Number of Completed Assignments (Graded 100%)'


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'average_grade')

    def average_grade(self, obj):
        return obj.studentassignment_set.aggregate(Avg('grade'))['grade__avg']

    average_grade.short_description = 'Average Grade'



@admin.register(StudentAssignment)
class StudentAssignmentAdmin(admin.ModelAdmin):
    pass

