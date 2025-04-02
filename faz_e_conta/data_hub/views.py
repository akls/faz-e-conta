import matplotlib.pyplot as plt
from .gerar_graficos import *

import io
import csv
import os
import json
import base64


from django.shortcuts import redirect, render
from .forms import *
from .models import *
from .auto_gen_form_views import *
from .auto_gen_id_views import *
from django.db.models import Model
from django.apps import apps
from datetime import date, datetime, time
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings



folder = "show_all/"



def index(request, counter:int=1):
    graficos = []
    graficos.append(ResponsavelEducativo_HorariosEntradaQuantidade())
    graficos.append(Vacina_Quantidade())
    
    return render(request, "index.html", {"counter":counter, "graficos": graficos})


def show_alunos(request):
    data = Aluno.objects.all()
    #head = [field.name for field in Aluno._meta.fields]
    
    head = ["aluno_id", "nome_proprio", "apelido", "processo", "numero_documento", "data_admissao"]
    
    # Melhorando a criação da lista de dicionários
    data_dict = list(data.values(*head))
    model = "Aluno"
    
    return render(request, f"{folder}show_alunos.html", {"head": head, "data_dict": data_dict, "id": head[0], "model": model})


def show_responsaveis_educativos(request):
    data = ResponsavelEducativo.objects.all()
    #head = [field.name for field in Aluno._meta.fields]
    
    head = ["responsavel_educativo_id", "nome_proprio", "apelido", "numero_documento", "data_nascimento", "aluno_id"]
    
    # Melhorando a criação da lista de dicionários
    data_dict = list(data.values(*head))
    model = "ResponsavelEducativo"
    
    return render(request, f"{folder}show_responsaveis_educativos.html", {"head": head, "data_dict": data_dict, "id": head[0], "model": model})


def show_vacinas(request):
    data = Vacinacao.objects.all()
    head = [field.name for field in Vacinacao._meta.fields]

    # Melhorando a criação da lista de dicionários
    data_dict = list(data.values(*head))
    model = "Vacinacao"
    
    return render(request, f"{folder}show_vacinas.html", {"head": head, "data_dict": data_dict, "id": head[0], "model": model})


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

