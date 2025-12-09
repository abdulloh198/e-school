from django_filters import rest_framework as django_filters
from .models import Users, Teachers

class UserFilter(django_filters.FilterSet):

    class Meta:
        model = Users
        fields = ['clas']


class TeacherFilter(django_filters.FilterSet):

    class Meta:
        model = Teachers
        fields = ['tch_id', 'name']


