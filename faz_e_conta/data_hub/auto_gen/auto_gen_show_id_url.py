from django.urls import path
from .. import views

def add_show_id_urlpatterns(urlpatterns):
    urlpatterns.append(path('aluno/<int:aluno_id>/', views.show_aluno_view, name='aluno_view'))
    urlpatterns.append(path('responsavel_educativo/<int:responsavel_educativo_id>/', views.show_responsavel_educativo_view, name='responsavel_educativo_view'))
    urlpatterns.append(path('aluno_saida/<int:aluno_saida_id>/', views.show_aluno_saida_view, name='aluno_saida_view'))
    urlpatterns.append(path('vacinacao/<int:vacinacao_id>/', views.show_vacinacao_view, name='vacinacao_view'))
    urlpatterns.append(path('despesa_fixa/<int:despesa_fixa_id>/', views.show_despesa_fixa_view, name='despesa_fixa_view'))
    urlpatterns.append(path('despesas_variavel/<int:despesas_variavel_id>/', views.show_despesas_variavel_view, name='despesas_variavel_view'))
    urlpatterns.append(path('salario/<int:salario_id>/', views.show_salario_view, name='salario_view'))
    urlpatterns.append(path('link_filiacao/<int:link_filiacao_id>/', views.show_link_filiacao_view, name='link_filiacao_view'))
    urlpatterns.append(path('sala/<int:sala_id>/', views.show_sala_view, name='sala_view'))
    urlpatterns.append(path('mensalidade_aluno/<int:mensalidade_aluno_id>/', views.show_mensalidade_aluno_view, name='mensalidade_aluno_view'))
    urlpatterns.append(path('aluno_financas/<int:aluno_financas_id>/', views.show_aluno_financas_view, name='aluno_financas_view'))
    urlpatterns.append(path('aluno_finacas_calc/<int:aluno_finacas_calc_id>/', views.show_aluno_finacas_calc_view, name='aluno_finacas_calc_view'))
    urlpatterns.append(path('funcionario/<int:funcionario_id>/', views.show_funcionario_view, name='funcionario_view'))
    urlpatterns.append(path('comparticipacao_mensal_ss/<int:comparticipacao_mensal_ss_id>/', views.show_comparticipacao_mensal_ss_view, name='comparticipacao_mensal_ss_view'))
    urlpatterns.append(path('vacina/<int:vacina_id>/', views.show_vacina_view, name='vacina_view'))
    urlpatterns.append(path('dose/<int:dose_id>/', views.show_dose_view, name='dose_view'))
    urlpatterns.append(path('divida/<int:divida_id>/', views.show_divida_view, name='divida_view'))
    urlpatterns.append(path('acordo/<int:acordo_id>/', views.show_acordo_view, name='acordo_view'))

    return urlpatterns
