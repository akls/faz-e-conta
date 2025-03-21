from django.urls import path

from . import views

urlpatterns = [
    path("", views.starter_page, name="starter_page"),
    path('alunos/', views.show_students, name='show_students'),
    path('alunos/inserir/', views.insert_student, name='insert_student'),
]
