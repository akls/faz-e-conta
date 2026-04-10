from django.urls import path
from . import views

def add_show_id_urlpatterns(urlpatterns):
    urlpatterns.append(path('aluno/<int:aluno_id>/', views.show_aluno_view, name='aluno_view'))
    urlpatterns.append(path('responsavel_educativo/<int:responsavel_educativo_id>/', views.show_responsavel_educativo_view, name='responsavel_educativo_view'))
    urlpatterns.append(path('sala/<int:sala_id>/', views.show_sala_view, name='sala_view'))
    urlpatterns.append(path('aluno_financas/<int:aluno_financas_id>/', views.show_aluno_financas_view, name='aluno_financas_view'))

    return urlpatterns
