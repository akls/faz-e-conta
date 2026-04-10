from django.urls import path
from . import views

def add_form_urlpatterns(urlpatterns):
    urlpatterns.append(path('insert_aluno/', views.insert_aluno_view, name='insert_aluno_view'))
    urlpatterns.append(path('insert_responsavel_educativo/', views.insert_responsavel_educativo_view, name='insert_responsavel_educativo_view'))

    return urlpatterns
