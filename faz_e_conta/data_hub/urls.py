from django.urls import path
from . import views
from .auto_gen_form_url import *
from .auto_gen_show_id_url import *

urlpatterns = [
    path('', views.starter_page, name="starter_page"),
    path('alunos/', views.show_students, name='show_students'),
    path('alunos_financas/', views.show_financas, name='show_aluno_financas'),
    path('contactos/', views.show_contactos, name='show_contactos'),
    path('salas/', views.show_salas, name='show_salas'),
    path('despesas/', views.show_despesas, name='show_despesas'),
    path('aluno/<int:aluno_id>/', views.show_student_details, name='show_student_details'),
]

urlpatterns = add_form_urlpatterns(urlpatterns)
urlpatterns = add_show_id_urlpatterns(urlpatterns)