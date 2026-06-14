from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'Class', ClassViewset)
router.register(r'Teachers', TeacherViewSet)
router.register(r'Students', StudentViewSet)
router.register(r'Gradebook', GradebookViewSet)
router.register(r'Comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
