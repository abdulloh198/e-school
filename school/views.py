from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models
from .filters import *
from .serializers import *
from .models import *
from rest_framework import filters
from django_filters import rest_framework as django_filters



class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teachers.objects.all()
    serializer_class = TeacherSerializer

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TeacherFilter
    search_fields = ['tch_id', 'name', 'lt_name', 'job']

    def list(self, request, *args, **kwargs):
        teacher = request.query_params.get('teacher', None)
        if teacher:
            self.queryset = self.queryset.filter(ustoz=teacher)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_teachers = Users.objects.filter(Users=instance.user).exclude(id=instance.id)[:5]
        related_serializer = TeacherSerializer(related_teachers, many=True)
        return Response({
            'teacher': serializer.data,
            'related_teachers': related_serializer.data
        })



class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserRatingSerializer

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = UserFilter
    search_fields = ['first_name', 'last_name', 'clas']


    def list(self, request, *args, **kwargs):
        student = request.query_params.get('user', None)
        if student:
            self.queryset = self.queryset.filter(uquvchi=student)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_users = Users.objects.filter(Users=instance.user).exclude(id=instance.id)[:5]
        related_serializer = UserRatingSerializer(related_users, many=True)
        return Response({
            'users': serializer.data,
            'related_users': related_serializer.data
        })


class DailyViewSet(viewsets.ModelViewSet):
    queryset = Daily.objects.all()
    serializer_class = DailySerializer

    @action(detail=False, methods=['get'])
    def ratings(self, request):
        queryset = Daily.objects.annotate(quarter=models.Avg('rating'))

        if queryset.count() == 0:
            return Response({"message": "No ratings found"}, status=404)

        serializer = DailySerializer(queryset, many=True)
        return Response(serializer.data)


class ThoughtsViewSet(viewsets.ModelViewSet):
    queryset = Thoughts.objects.all()
    serializer_class = ThoughtSerializer

