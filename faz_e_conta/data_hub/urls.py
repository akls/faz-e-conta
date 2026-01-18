from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
]

testes = [
    path('galeria/', views.galeria, name='galeria'),
]



financas = [
    
]

user = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user_management/', views.user_management, name='user_management'),
]

alunos = [
    path('alunos/', views.dashboard_alunos, name='alunos'),
]

reports = [
    path('reports/', views.reports, name='reports'),
    path('<str:model>/gerar-pdf/', views.gerar_pdf, name='gerar_pdf'),
    path('gerar-pdf-aluno/<int:aluno_id>/', views.gerar_pdf_aluno, name='gerar_pdf_aluno'),
    path('report/aluno_sala/', views.reportAlunoSala, name='report_aluno_sala'),
    path('gerar-pdf-mensal/', views.reportMensal, name='report_mensal'),
    path('gerar-pdf-mensal/<int:month>/<int:year>/', views.reportMensal, name='report_mensal'),
]


'''
URLs added
'''
urlpatterns += testes

urlpatterns += user
urlpatterns += reports
urlpatterns += financas
urlpatterns += alunos

