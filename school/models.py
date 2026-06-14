from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Teacher(models.Model):
    teacher_id = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    name = models.CharField(max_length=123)
    last_name = models.CharField(max_length=123)
    job = models.CharField(max_length=123)

    def __str__(self):
        return self.name


class Class(models.Model):
    class_id = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    name = models.CharField(max_length=4)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name



class Gradebook(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])


    def __str__(self):
        return f"{self.student}'s daily"


class Comment(models.Model):
    owner = models.CharField(max_length=120, null=False)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    text = models.TextField(max_length=255)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"by {self.owner} to {self.student}"





