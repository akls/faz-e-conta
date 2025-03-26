from django.shortcuts import redirect, render
from .forms import *
from .models import *
from .auto_gen_form_views import *
from .auto_gen_id_views import *
from django.db.models import Model
import csv
from django.apps import apps


def index(request):
    return render(request, "index.html", {"model": "Aluno"})


def show_alunos(request):
    data = Aluno.objects.all()
    #head = [field.name for field in Aluno._meta.fields]
    
    head = ["aluno_id", "nome_proprio", "apelido", "processo", "numero_documento", "data_admissao"]
    
    # Melhorando a criação da lista de dicionários
    data_dict = list(data.values(*head))
    model = "Aluno"
    
    return render(request, "show_alunos.html", {"head": head, "data_dict": data_dict, "id": head[0], "model": model})


def show_responsaveis_educativos(request):
    data = ResponsavelEducativo.objects.all()
    #head = [field.name for field in Aluno._meta.fields]
    
    head = ["responsavel_educativo_id", "nome_proprio", "apelido", "numero_documento", "data_nascimento", "aluno_id"]
    
    # Melhorando a criação da lista de dicionários
    data_dict = list(data.values(*head))
    model = "ResponsavelEducativo"
    
    return render(request, "show_responsaveis_educativos.html", {"head": head, "data_dict": data_dict, "id": head[0], "model": model})

    

def export(request, model):
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
    response['Content-Disposition'] = f'attachment; filename="{model_class.__name__.lower()}.csv"'

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

