from django.urls import path
from . import views

def add_show_id_urlpatterns(urlpatterns):
    urlpatterns.append(path('aluno/<int:aluno_id>/', views.show_aluno_view, name='aluno_view'))
    urlpatterns.append(path('responsavel_educativo/<int:responsavel_educativo_id>/', views.show_responsavel_educativo_view, name='responsavel_educativo_view'))
    urlpatterns.append(path('aluno_saida/<int:aluno_saida_id>/', views.show_aluno_saida_view, name='aluno_saida_view'))
    urlpatterns.append(path('vacinacao/<int:vacinacao_id>/', views.show_vacinacao_view, name='vacinacao_view'))
    urlpatterns.append(path('despesa/<int:despesa_id>/', views.show_despesa_view, name='despesa_view'))
    urlpatterns.append(path('salario/<int:salario_id>/', views.show_salario_view, name='salario_view'))
    urlpatterns.append(path('filiacao/<int:filiacao_id>/', views.show_filiacao_view, name='filiacao_view'))

    return urlpatterns
