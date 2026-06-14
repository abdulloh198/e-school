from django_filters import rest_framework as django_filters
from .models import *


class ClassFilter(django_filters.FilterSet):

    class Meta:
        model = Class
        fields = ['name', 'teacher']


class StudentFilter(django_filters.FilterSet):

    class Meta:
        model = Student
        fields = ['first_name', 'class_name']


class TeacherFilter(django_filters.FilterSet):

    class Meta:
        model = Teacher
        fields = ['name', 'job']


