from django.urls import path
from . import views

def add_urlpatterns(urlpatterns):
    urlpatterns.append(path('insert_aluno/', views.insert_aluno_view, name='insert_aluno_view'))
    urlpatterns.append(path('insert_responsavel_educativo/', views.insert_responsavel_educativo_view, name='insert_responsavel_educativo_view'))
    urlpatterns.append(path('insert_aluno_saida/', views.insert_aluno_saida_view, name='insert_aluno_saida_view'))
    urlpatterns.append(path('insert_vacinacao/', views.insert_vacinacao_view, name='insert_vacinacao_view'))
    urlpatterns.append(path('insert_despesa/', views.insert_despesa_view, name='insert_despesa_view'))
    urlpatterns.append(path('insert_salario/', views.insert_salario_view, name='insert_salario_view'))
    urlpatterns.append(path('insert_filiacao/', views.insert_filiacao_view, name='insert_filiacao_view'))

    return urlpatterns
