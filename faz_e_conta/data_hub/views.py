from django.shortcuts import redirect, render
from .forms import *
from .models import *
from .auto_gen_form_views import *
from .auto_gen_id_views import *
from django.db.models import Q  # Import Q for dynamic filtering


def show_students(request):
    data = Aluno.objects.all()
    query = request.GET.get("q", "")  # Get search query from the URL
    if query:
        data = Aluno.objects.filter(
            Q(nome_proprio__icontains=query) | 
            Q(apelido__icontains=query) | 
            Q(processo__icontains=query)
        )  # Search across multiple fields
    #head = [field.name for field in Aluno._meta.fields]
    
    head = ["aluno_id", "nome_proprio", "apelido", "processo", "numero_documento", "data_admissao"]
    
    # Melhorando a criação da lista de dicionários
    data_dict = list(data.values(*head))
    
    return render(request, "show_students.html", {"head": head, "data_dict": data_dict, "id": head[0]})