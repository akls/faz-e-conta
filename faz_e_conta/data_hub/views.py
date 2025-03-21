from django.shortcuts import redirect, render
from .forms import *
from .models import *
from .auto_gen_form_views import *
from .auto_gen_id_views import *

def index(request):
    return render(request, "index.html")

def show_students(request):
    data = Aluno.objects.all()
    #head = [field.name for field in Aluno._meta.fields]
    
    head = ["aluno_id", "nome_proprio", "apelido", "processo", "numero_documento", "data_admissao"]
    
    # Melhorando a criação da lista de dicionários
    data_dict = list(data.values(*head))
    
    return render(request, "show_students.html", {"head": head, "data_dict": data_dict, "id": head[0]})


def show_responsaveis_educativos(request):
    data = ResponsavelEducativo.objects.all()
    #head = [field.name for field in Aluno._meta.fields]
    
    head = ["responsavel_educativo_id", "nome_proprio", "apelido", "numero_documento", "data_nascimento", "aluno_id"]
    
    # Melhorando a criação da lista de dicionários
    data_dict = list(data.values(*head))
    
    return render(request, "show_responsaveis_educativos.html", {"head": head, "data_dict": data_dict, "id": head[0]})