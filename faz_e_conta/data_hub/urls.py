from django.urls import path

from . import views

urlpatterns = [
    path('', views.show_students, name='show_students'),
    path('insert/', views.insert_student, name='insert_student'),
    path('<int:aluno_id>/', views.show_student, name='show_student'),
]
