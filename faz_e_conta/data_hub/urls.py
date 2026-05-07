from django.urls import path
from . import views
from .auto_gen_form_url import *
from .auto_gen_show_id_url import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Landing page
    path('', views.starter_page, name="starter_page"),




    #Login/criar conta
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('insert_user/', views.insert_user, name='insert_user'),




    # Show
    path('alunos/', views.show_students, name='show_students'),
    path('alunos_financas/', views.show_financas, name='show_aluno_financas'),
    path('contactos/', views.show_contactos, name='show_contactos'),
    path('salas/', views.show_salas, name='show_salas'),
    path('despesas/', views.show_despesas, name='show_despesas'),
    path('aluno/<int:aluno_id>/', views.show_student_details, name='show_student_details'),
    path('responsavel/<int:responsavel_id>/', views.show_contactos_details, name='show_contactos_details'),
    path('saude_financeira', views.show_saude_fianceira, name='show_saude_financeira'),




    # Insert
    path('insert_despesas/<str:tipo_despesa>/', views.insert_despesa_view, name='insert_despesa_view'),
    path('insert_sala/', views.insert_sala_view, name='insert_sala_view'),
    path('insert_financas/', views.insert_financas, name='insert_financas'),




    # Editar
    path('aluno/<int:aluno_id>/editar/', views.edit_student, name='edit_student'),
    path('responsavel/<int:responsavel_id>/editar/', views.edit_responsavel_educativo, name='edit_responsavel_educativo'),
    path("salas/<int:sala_id>/edit", views.edit_sala, name="edit_sala"),
    path('alunos_financas/<int:financa_id>', views.edit_financas, name='edit_financas'),
    path('despesas/fixas/<int:despesaFixa_id>', views.edit_despesasFixas, name='edit_despesasFixas'),
    path('despesas/variaveis/<int:despesaVariavel_id>', views.edit_despesasVariaveis, name='edit_despesasVariaveis'),
]

urlpatterns = add_form_urlpatterns(urlpatterns)
urlpatterns = add_show_id_urlpatterns(urlpatterns)