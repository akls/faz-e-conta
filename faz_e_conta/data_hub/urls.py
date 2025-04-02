from django.urls import path
from . import views
from .auto_gen_form_url import *
from .auto_gen_show_id_url import *

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:counter>', views.index, name='index'),
    
    path('export_csv/<str:model>/', views.export_csv, name='export_csv'),
    path('export_json/<str:model>/', views.export_json, name='export_json'),
    
    path('alunos/', views.show_alunos, name='show_alunos'),
    path('responsaveis_educativos/', views.show_responsaveis_educativos, name='show_responsaveis_educativos'),
    path('vacinas/', views.show_vacinas, name='show_vacinas'),
]

urlpatterns = add_form_urlpatterns(urlpatterns)
urlpatterns = add_show_id_urlpatterns(urlpatterns)