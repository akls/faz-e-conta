from django.urls import path
from . import views
from .auto_gen_form_url import *
from .auto_gen_show_id_url import *

urlpatterns = [
    path('', views.starter_page, name="starter_page"),
    path('alunos/', views.show_students, name='show_students'),
    path('alunos_financas/', views.show_financas,name='show_aluno_financas'),
]

urlpatterns = add_form_urlpatterns(urlpatterns)
urlpatterns = add_show_id_urlpatterns(urlpatterns)