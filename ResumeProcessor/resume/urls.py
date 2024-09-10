from django.urls import path
from . import views

urlpatterns = [
    path('extract_resume/', views.extract_resume, name='extract_resume'),
]
