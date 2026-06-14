from rest_framework import serializers
from .models import *


class ClasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = "__all__"


class GradebookSerializer(serializers.ModelSerializer):
    quarter = serializers.FloatField(read_only=True, required=False)

    class Meta:
        model = Gradebook
        fields = ['student', 'rating', 'quarter']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"

