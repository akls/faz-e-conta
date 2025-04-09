from django.urls import path
from . import views

def add_form_urlpatterns(urlpatterns):
    urlpatterns.append(path('insert_aluno/', views.insert_aluno_view, name='insert_aluno_view'))
    urlpatterns.append(path('insert_responsavel_educativo/', views.insert_responsavel_educativo_view, name='insert_responsavel_educativo_view'))
    urlpatterns.append(path('insert_aluno_saida/', views.insert_aluno_saida_view, name='insert_aluno_saida_view'))
    urlpatterns.append(path('insert_vacinacao/', views.insert_vacinacao_view, name='insert_vacinacao_view'))
    urlpatterns.append(path('insert_despesa_fixa/', views.insert_despesa_fixa_view, name='insert_despesa_fixa_view'))
    urlpatterns.append(path('insert_despesas_variavel/', views.insert_despesas_variavel_view, name='insert_despesas_variavel_view'))
    urlpatterns.append(path('insert_salario/', views.insert_salario_view, name='insert_salario_view'))
    urlpatterns.append(path('insert_link_filiacao/', views.insert_link_filiacao_view, name='insert_link_filiacao_view'))
    urlpatterns.append(path('insert_sala/', views.insert_sala_view, name='insert_sala_view'))
    urlpatterns.append(path('insert_mensalidade_aluno/', views.insert_mensalidade_aluno_view, name='insert_mensalidade_aluno_view'))
    urlpatterns.append(path('insert_aluno_financas/', views.insert_aluno_financas_view, name='insert_aluno_financas_view'))
    urlpatterns.append(path('insert_aluno_finacas_calc/', views.insert_aluno_finacas_calc_view, name='insert_aluno_finacas_calc_view'))
    urlpatterns.append(path('insert_funcionario/', views.insert_funcionario_view, name='insert_funcionario_view'))
    urlpatterns.append(path('insert_comparticipacao_mensal_ss/', views.insert_comparticipacao_mensal_ss_view, name='insert_comparticipacao_mensal_ss_view'))
    urlpatterns.append(path('insert_vacina/', views.insert_vacina_view, name='insert_vacina_view'))
    urlpatterns.append(path('insert_dose/', views.insert_dose_view, name='insert_dose_view'))
    urlpatterns.append(path('insert_divida/', views.insert_divida_view, name='insert_divida_view'))
    urlpatterns.append(path('insert_acordo/', views.insert_acordo_view, name='insert_acordo_view'))

    return urlpatterns
