from django.urls import path
from . import views
from .auto_gen_form_url import *
from .auto_gen_show_id_url import *

urlpatterns = [
    path('', views.show_students, name='index'),
    path('view_students/', views.show_students, name='show_students'),
]

urlpatterns = add_form_urlpatterns(urlpatterns)
urlpatterns = add_show_id_urlpatterns(urlpatterns)