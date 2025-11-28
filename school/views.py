from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models
from .filters import UserFilter
from .serializers import *
from .models import *
from rest_framework import filters
from django_filters import rest_framework as django_filters



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
            'product': serializer.data,
            'related_products': related_serializer.data
        })


class DailyViewSet(viewsets.ModelViewSet):
    queryset = Daily.objects.all()
    serializer_class = DailySerializer

    @action(detail=False, methods=['get'])
    def ratings(self, request):
        queryset = Users.objects.annotate(
            average_rating=models.Avg('daily__rating')
        )

        if queryset.count() == 0:
            return Response({"message": "No ratings found"}, status=404)

        serializer = UserRatingSerializer(queryset, many=True)
        return Response(serializer.data)


class ThoughtsViewSet(viewsets.ModelViewSet):
    queryset = Thoughts.objects.all()
    serializer_class = ThoughtSerializer

