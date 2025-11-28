from django_filters import rest_framework as django_filters
from .models import Users

class UserFilter(django_filters.FilterSet):

    class Meta:
        model = Users
        fields = ['clas']


