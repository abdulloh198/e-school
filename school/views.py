from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from . import models
from .filters import *
from .serializers import *
from .models import *
from rest_framework import filters
from django_filters import rest_framework as django_filters


class ClassViewset(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClasSerializer

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ClassFilter
    search_fields = ['name', 'teacher']

    @action(detail=True, methods=['get'])
    def student_count(self, request, pk=None):
        class_instance = self.get_object()
        student_count = Student.objects.filter(class_name=class_instance).count()
        return Response({'student_count': student_count})

    @action(detail=True, methods=['get'])
    def student_ratings(self, request, pk=None):
        class_instance = self.get_object()
        students = Student.objects.filter(class_name=class_instance)
        student_ratings = []
        for student in students:
            gradebooks = Gradebook.objects.filter(student=student)
            average_rating = gradebooks.aggregate(models.Avg('rating'))['rating__avg']
            student_ratings.append({'student': student.first_name, 'average_rating': average_rating})
        student_ratings.sort(key=lambda x: x['average_rating'], reverse=True)
        return Response(student_ratings)


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TeacherFilter
    search_fields = ['name', 'last_name', 'job']

    def list(self, request, *args, **kwargs):
        teacher = request.query_params.get('teacher', None)
        if teacher:
            self.queryset = self.queryset.filter(ustoz=teacher)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_teachers = Teacher.objects.filter(teacher_id=instance.user).exclude(id=instance.id)[:5]
        related_serializer = TeacherSerializer(related_teachers, many=True)
        return Response({
            'teacher': serializer.data,
            'related_teachers': related_serializer.data
        })


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = StudentFilter
    search_fields = ['first_name', 'last_name', 'class_name', 'teacher']

    def list(self, request, *args, **kwargs):
        student = request.query_params.get('user', None)
        if student:
            self.queryset = self.queryset.filter(uquvchi=student)
        return super().list(request, *args, **kwargs)


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        teacher = instance.teacher
        teacher_serializer = TeacherSerializer(teacher)
        gradebooks = Gradebook.objects.filter(student=instance)
        gradebook_serializer = GradebookSerializer(gradebooks, many=True)
        return Response({
            'student': serializer.data,
            'teacher': teacher_serializer.data,
            'gradebook': gradebook_serializer.data
        })


class GradebookViewSet(viewsets.ModelViewSet):
    queryset = Gradebook.objects.all()
    serializer_class = GradebookSerializer

    @action(detail=False, methods=['get'])
    def ratings(self, request):
        queryset1 = Gradebook.objects.values('student_id').annotate(quarter=models.Avg('rating'))

        return Response(queryset1)

    @action(detail=False, methods=['get'])
    def top_students(self, request):
        queryset1 = Gradebook.objects.values('student_id').annotate(average_rating=models.Avg('rating')).order_by('-average_rating')[:5]
        return Response(queryset1)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


