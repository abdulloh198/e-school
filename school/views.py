from django.contrib.admin.actions import delete_selected
from django.db.models.aggregates import Avg
from django.db.models.fields import return_None
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
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
        related_teacher = Teachers.objects.filter(Teachers=instance.teacher).exclude(id=instance.id)[:5]
        related_serializer = (related_teacher)
        return Response({
            'teacher': serializer.data,
            'related_teachers': related_serializer.data
        })



class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = UserFilter
    seachr_fields = ['first_name', 'last_name', 'clas']

    def list(self, request, *args, **kwargs):
        student = request.query_params.get('user', None)
        if student:
            self.queryset = self.queryset.filter(uquvchi=student)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_users = Users.objects.filter(Users=instance.user).exclude(id=instance.id)[:5]
        related_serializer = (related_users)
        return Response({
            'student': serializer.data,
            'related_student': related_serializer.data
        })

    @action(detail=True, methods=['get'])
    def techr(self, request, pk=None):
        user = get_object_or_404(Users, id=pk)
        teacher = user.teacher

        return Response({
            "teacher": teacher
        })


class DailyViewSet(viewsets.ModelViewSet):
    queryset = Daily.objects.all()
    serializer_class = dailyserializer


    @action(detail=False, methods=['get'])
    def ratings(self, request):
        queryset = Daily.objects.aggregate(quarter=Avg('rating'))

        if queryset['quarter'] is None:
            return Response({"message": "No ratings"}, status=404)

        return Response({
            "quarter": queryset['quarter']
        })


class ThoughtsViewSet(viewsets.ModelViewSet):
    queryset = Thoughts.objects.all()
    serializer_class = thoughtserializer

    @action(detail=True, methods=['get'])
    def level(self, request, pk=None):
        comment = get_object_or_404(Thoughts, id=pk)
        rating = comment.rating

        if rating >= 5:
            status = "alochi"

        else:
            status = "qoniqarsiz"

        return Response({
            "rating": rating,
            "comment": status
        })
