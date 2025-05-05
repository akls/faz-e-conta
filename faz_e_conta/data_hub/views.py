from .gerar_graficos import *

import csv
import os
import json

from .reports.reports import * 

from django.shortcuts import redirect, render
from .forms import *
from .models import *

from .auto_gen.auto_gen_form_views import *
from .auto_gen.auto_gen_id_views import *

from django.db.models import Model
from django.apps import apps
from datetime import date, datetime, time
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.conf import settings

from django.contrib.auth.forms import UserCreationForm # Certifique-se que este import está presente


from .reports.reports import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from django.db.models import Q  # Import Q for dynamic filtering


folder = "show_all/"

@login_required
def profile(request):
    return render(request, "auth/profile.html", {"user": request.user})

def index(request, counter: int = 1):
    folder_path = "resources/graficos"
    absolute_path = os.path.join(settings.BASE_DIR, folder_path)

    graficos = []
    if os.path.exists(absolute_path):
        for f in os.listdir(absolute_path):
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                graficos.append(f"graficos/{f}")  # caminho relativo a /media/

    return render(request, "index.html", {
        "counter": counter,
        "graficos": graficos
    })

def show_alunos(request):
    query = request.GET.get("q", "")  # Get search query from the URL
    sala_filter = request.GET.get("sala", "")  # Get sala filter from the URL

    # Base queryset
    data = Aluno.objects.select_related('sala_id').all()

    # Apply search filter
    if query:
        data = data.filter(
            Q(nome_proprio__icontains=query) | 
            Q(apelido__icontains=query) | 
            Q(processo__icontains=query)
        )

    # Apply sala_valencia or sala_nome filter
    if sala_filter:
        data = data.filter(
            Q(sala_id__sala_valencia__icontains=sala_filter) |
            Q(sala_id__sala_nome__icontains=sala_filter)
        )

    # Define the fields to display
    head = ["aluno_id", "nome_proprio", "apelido", "processo", "numero_documento", "data_admissao", "sala_id__sala_valencia", "sala_id__sala_nome"]
    data_dict = list(data.values(*head))

    # Get unique sala_valencia and sala_nome values for the dropdown
    salas = Sala.objects.values_list("sala_valencia", flat=True).distinct()
    sala_nomes = Sala.objects.values_list("sala_nome", flat=True).distinct()

    # Render the template with context
    context = {
        "head": head,
        "data_dict": data_dict,
        "id": head[0],
        "query": query,
        "sala_filter": sala_filter,
        "salas": salas,
        "sala_nomes": sala_nomes,
    }
    
    return render(request,  f"{folder}show_alunos.html", context)


def show_responsaveis_educativos(request):
    data = ResponsavelEducativo.objects.all()    
    head = ["responsavel_educativo_id", "nome_proprio", "apelido", "numero_documento", "data_nascimento", "aluno_id"]
    
    # Melhorando a criação da lista de dicionários
    data_dict = list(data.values(*head))
    model = "ResponsavelEducativo"
    file_exists = json_exist(ResponsavelEducativo._meta.db_table.lower())
    
    return render(request, f"{folder}show_responsaveis_educativos.html", {"head": head, "data_dict": data_dict, "id": head[0], "model": model, 'file_exists': file_exists})

def show_vacinas(request):
    data = Vacinacao.objects.all()
    head = [field.name for field in Vacinacao._meta.fields]

    # Melhorando a criação da lista de dicionários
    data_dict = list(data.values(*head))
    model = "Vacinacao"
    file_exists = json_exist(Vacinacao._meta.db_table.lower())
    
    return render(request, f"{folder}show_vacinas.html", {"head": head, "data_dict": data_dict, "id": head[0], "model": model, 'file_exists': file_exists})

def reports(request):
    folder = "report/"
    return render(request, f"{folder}reports_page.html")

# added
def show_aluno_new(request):
    query = request.GET.get("q", "")  # Get search query from the URL
    sala_filter = request.GET.get("sala", "")  # Get sala filter from the URL

    # Base queryset
    data = Aluno.objects.all()

    # Apply search filter
    if query:
        data = data.filter(
            Q(nome_proprio__icontains=query) |
            Q(apelido__icontains=query)
        )

    # Apply sala_valencia filter
    if sala_filter:
        data = data.filter(sala_id__sala_valencia__icontains=sala_filter)

    # Define the fields to display
    head = ["nome_proprio", "apelido", "processo", "sala_id__sala_valencia"]
    data_dict = list(data.values(*head))

    # Get unique sala_valencia values for the dropdown
    salas = Sala.objects.values_list("sala_valencia", flat=True).distinct()

    # Render the template with context
    context = {
        "head": head,
        "data_dict": data_dict,
        "id": "nome_proprio",  # Use student name as identifier
        "query": query,
        "sala_filter": sala_filter,
        "salas": salas,
    }
    return render(request, "show/show_aluno.html", context)


# Exports
def export_json(request, model):
    model_class = None
    for app in apps.get_app_configs():
        try:
            model_class = apps.get_model(app.label, model)
            break
        except LookupError:
            continue

    if not model_class:
        return HttpResponse(f'Modelo "{model}" não encontrado.', status=404)

    # Obter os dados da classe (modelo)
    model_data = model_class.objects.all()

    # Criar a estrutura de dados JSON
    data = []
    field_names = [field.name for field in model_class._meta.fields]
    
    def serialize_value(value):
        if isinstance(value, (date, datetime, time)):
            return str(value)  # Converter datas e horários para string
        if isinstance(value, Model):  # Verifica se é um objeto relacionado
            return value.pk  # Usa o ID do objeto relacionado
        return value
    
    for obj in model_data:
        item = {field: serialize_value(getattr(obj, field)) for field in field_names}
        data.append(item)

    # Definir o caminho para salvar o arquivo no diretório "resources/jsons"
    json_dir = os.path.join(settings.BASE_DIR, 'resources', 'jsons')
    os.makedirs(json_dir, exist_ok=True)
    file_path = os.path.join(json_dir, f'{model_class._meta.db_table.lower()}.json')

    # Salvar o JSON no arquivo
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    # Redirecionar de volta para a página anterior
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def export_csv(request, model):
    # Tente procurar o modelo no Django, usando o nome passado
    model_class = None
    for app in apps.get_app_configs():
        try:
            # Tente obter o modelo com o nome 'model_name' dentro do app
            model_class = apps.get_model(app.label, model)
            break  # Modelo encontrado, podemos parar a busca
        except LookupError:
            # Se o modelo não for encontrado neste app, continue buscando nos outros apps
            continue

    # Verifique se encontramos o modelo
    if not model_class:
        return HttpResponse(f'Modelo "{model}" não encontrado.', status=404)

    # Criar a resposta HTTP com o tipo de conteúdo correto para CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{model_class._meta.db_table.lower()}.csv"'

    # Criar o escritor CSV
    writer = csv.writer(response)

    # Definir os campos do cabeçalho do CSV (os nomes dos campos do modelo)
    field_names = [field.name for field in model_class._meta.fields]
    writer.writerow(field_names)

    # Obter os dados da classe (modelo)
    model_data = model_class.objects.all()

    # Iterar sobre os dados e escrever as linhas no CSV
    for obj in model_data:
        row = []
        for field in field_names:
            value = getattr(obj, field)
            # Verificar se o valor é um objeto relacionado (chave estrangeira ou similar)
            if isinstance(value, Model):  # Verifica se é uma instância de um modelo
                # Pode-se decidir aqui qual atributo do objeto relacionado exportar, por exemplo, o ID
                value = value.pk  # Ou qualquer outro atributo relacionado que queira exportar

            row.append(value)
        writer.writerow(row)

    return response

def download_json(request, model):
    for app in apps.get_app_configs():
        try:
            model_class = apps.get_model(app.label, model)
            break
        except LookupError:
            continue
    
    table = model_class._meta.db_table.lower()
    
    json_dir = os.path.join(settings.BASE_DIR, 'resources', 'jsons')
    os.makedirs(json_dir, exist_ok=True)
    json_file_path = os.path.join(json_dir, f'{table.lower()}.json')
    
    if os.path.exists(json_file_path):
        return FileResponse(open(json_file_path, 'rb'), as_attachment=True, filename=f"{table.lower()}.json")
    
    raise Http404("Ficheiro não encontrado")

def delete_json(request, model):
    # Define o caminho do arquivo JSON
    for app in apps.get_app_configs():
        try:
            model_class = apps.get_model(app.label, model)
            break
        except LookupError:
            continue
    
    table = model_class._meta.db_table.lower()
    
    json_dir = os.path.join(settings.BASE_DIR, 'resources', 'jsons')
    os.makedirs(json_dir, exist_ok=True)
    file_path = os.path.join(json_dir, f'{table.lower()}.json')
    

    # Verifica se o arquivo existe antes de tentar excluir
    if os.path.exists(file_path):
        try:
            os.remove(file_path)  # Deleta o arquivo
        except Exception as e:
            pass
    else:
        pass
    return redirect(request.META.get("HTTP_REFERER", "/"))  # Redireciona para a página anterior



# User
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "user/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def register(request):
    if request.method == "POST":
        # Usa UserCreationForm para processar o POST
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # Salva o novo usuário
            username = form.cleaned_data.get('username') # Opcional: pegar o username para a mensagem
            messages.success(request, f"Conta para '{username}' criada com sucesso! Faça o login.")
            return redirect("login") # Redireciona para a página de login após o sucesso
        else:
             messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = UserCreationForm()
    return render(request, "user/register.html", {"form": form})


