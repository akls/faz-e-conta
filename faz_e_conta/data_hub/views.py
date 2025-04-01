from django.shortcuts import redirect, render
from .forms import *
from .models import *
from .auto_gen_form_views import *
from .auto_gen_id_views import *
from django.db.models import Q  # Import Q for dynamic filtering

def starter_page(request):
    return render(request, "starter_page.html")

def show_students(request):
    query = request.GET.get("q", "")  # Get search query from the URL
    sala_filter = request.GET.get("sala", "")  # Get sala filter from the URL

    # Base queryset
    data = Aluno.objects.all()

    # Apply search filter
    if query:
        data = data.filter(
            Q(nome_proprio__icontains=query) | 
            Q(apelido__icontains=query) | 
            Q(processo__icontains=query)
        )

    # Apply sala_valencia filter
    if sala_filter:
        data = data.filter(sala_id__sala_valencia__icontains=sala_filter)

    # Define the fields to display
    head = ["aluno_id", "nome_proprio", "apelido", "processo", "numero_documento", "data_admissao", "sala_id__sala_valencia"]
    data_dict = list(data.values(*head))

    # Get unique sala_valencia values for the dropdown
    salas = Sala.objects.values_list("sala_valencia", flat=True).distinct()

    # Render the template with context
    context = {
        "head": head,
        "data_dict": data_dict,
        "id": head[0],
        "query": query,
        "sala_filter": sala_filter,
        "salas": salas,
    }
    return render(request, "show_students.html", context)

def show_financas(request):
    query = request.GET.get("q", "")  # Get search query from the URL

    # Base queryset
    data = AlunoFinancas.objects.all()

    # Apply search filter by student ID
    if query:
        data = data.filter(aluno_id__aluno_id__icontains=query)

    # Define the fields to display
    head = ["ano_letivo", "despesa_anual", "rendim_líquido", "aluno_id__nome_proprio", "aluno_id__apelido", "aluno_id__numero_documento"]
    data_dict = list(data.values(*head))

    # Render the template with context
    context = {
        "head": head,
        "data_dict": data_dict,
        "id": "aluno_id__nome_proprio",  # Use student name as identifier
        "query": query,
    }
    return render(request, "show_aluno_financas.html", context)
