from rest_framework import serializers
from .models import *


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teachers
        fields = "__all__"


class UserRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['id','first_name', 'last_name', 'clas']


class DailySerializer(serializers.ModelSerializer):
    quarter = serializers.FloatField(read_only=True, required=False)

    class Meta:
        model = Daily
        fields = ['user', 'rating', 'quarter']


class ThoughtSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thoughts
        fields = "__all__"
