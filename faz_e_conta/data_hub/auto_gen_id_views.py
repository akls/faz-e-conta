from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import *

from django.http import Http404
from django.http import HttpResponse

def show_aluno_view(request, aluno_id):
    try:
        data = Aluno.objects.get(aluno_id=aluno_id)  # Verifique se 'id' é o nome correto do campo
    except Aluno.DoesNotExist:
        return HttpResponse(f'<h1>Aluno with id= {aluno_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name.replace('_id','_id_id') for field in Aluno._meta.fields]

    for i in range(1, len(head)):
        if head[i].endswith('_id_id'):
            related_model_name = head[i].replace('_id_id', '')
            related_model = globals()[related_model_name.capitalize()]
            related_instance = related_model.objects.get(pk=data.__dict__.get(head[i]))
            data.__dict__[head[i]] = related_instance
    data_dict = {head[i]: data.__dict__.get(head[i], None) for i in range(1, len(head))}

    return render(request, 'show_aluno.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_responsavel_educativo_view(request, responsavel_educativo_id):
    try:
        data = ResponsavelEducativo.objects.get(responsavel_educativo_id=responsavel_educativo_id)  # Verifique se 'id' é o nome correto do campo
    except ResponsavelEducativo.DoesNotExist:
        return HttpResponse(f'<h1>Responsavel Educativo with id= {responsavel_educativo_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name.replace('_id','_id_id') for field in ResponsavelEducativo._meta.fields]

    for i in range(1, len(head)):
        if head[i].endswith('_id_id'):
            related_model_name = head[i].replace('_id_id', '')
            related_model = globals()[related_model_name.capitalize()]
            related_instance = related_model.objects.get(pk=data.__dict__.get(head[i]))
            data.__dict__[head[i]] = related_instance
    data_dict = {head[i]: data.__dict__.get(head[i], None) for i in range(1, len(head))}

    return render(request, 'show_responsavel_educativo.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_sala_view(request, sala_id):
    try:
        data = Sala.objects.get(sala_id=sala_id)  # Verifique se 'id' é o nome correto do campo
    except Sala.DoesNotExist:
        return HttpResponse(f'<h1>Sala with id= {sala_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name.replace('_id','_id_id') for field in Sala._meta.fields]

    for i in range(1, len(head)):
        if head[i].endswith('_id_id'):
            related_model_name = head[i].replace('_id_id', '')
            related_model = globals()[related_model_name.capitalize()]
            related_instance = related_model.objects.get(pk=data.__dict__.get(head[i]))
            data.__dict__[head[i]] = related_instance
    data_dict = {head[i]: data.__dict__.get(head[i], None) for i in range(1, len(head))}

    return render(request, 'show_sala.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_aluno_financas_view(request, aluno_financas_id):
    try:
        data = AlunoFinancas.objects.get(aluno_financas_id=aluno_financas_id)  # Verifique se 'id' é o nome correto do campo
    except AlunoFinancas.DoesNotExist:
        return HttpResponse(f'<h1>Aluno Financas with id= {aluno_financas_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name.replace('_id','_id_id') for field in AlunoFinancas._meta.fields]

    for i in range(1, len(head)):
        if head[i].endswith('_id_id'):
            related_model_name = head[i].replace('_id_id', '')
            related_model = globals()[related_model_name.capitalize()]
            related_instance = related_model.objects.get(pk=data.__dict__.get(head[i]))
            data.__dict__[head[i]] = related_instance
    data_dict = {head[i]: data.__dict__.get(head[i], None) for i in range(1, len(head))}

    return render(request, 'show_aluno_financas.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

