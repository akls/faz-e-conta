from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Aluno, Responsavel_educativo, Aluno_saida, Vacinacao, Despesa, Salario, Filiacao
from .forms import AlunoForm, Responsavel_educativoForm, Aluno_saidaForm, VacinacaoForm, DespesaForm, SalarioForm, FiliacaoForm

def show_aluno_view(request, aluno_id):
    data = Aluno.objects.get(aluno_id=aluno_id)
    head = [field.name for field in Aluno._meta.fields]
    data_dict = {head[i]: data.__dict__[head[i]] for i in range(1, len(head))}
    return render(request, 'show_aluno.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_responsavel_educativo_view(request, responsavel_educativo_id):
    data = Responsavel_educativo.objects.get(responsavel_educativo_id=responsavel_educativo_id)
    head = [field.name for field in Responsavel_educativo._meta.fields]
    data_dict = {head[i]: data.__dict__[head[i]] for i in range(1, len(head))}
    return render(request, 'show_responsavel_educativo.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_aluno_saida_view(request, aluno_saida_id):
    data = Aluno_saida.objects.get(aluno_saida_id=aluno_saida_id)
    head = [field.name for field in Aluno_saida._meta.fields]
    data_dict = {head[i]: data.__dict__[head[i]] for i in range(1, len(head))}
    return render(request, 'show_aluno_saida.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_vacinacao_view(request, vacinacao_id):
    data = Vacinacao.objects.get(vacinacao_id=vacinacao_id)
    head = [field.name for field in Vacinacao._meta.fields]
    data_dict = {head[i]: data.__dict__[head[i]] for i in range(1, len(head))}
    return render(request, 'show_vacinacao.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_despesa_view(request, despesa_id):
    data = Despesa.objects.get(despesa_id=despesa_id)
    head = [field.name for field in Despesa._meta.fields]
    data_dict = {head[i]: data.__dict__[head[i]] for i in range(1, len(head))}
    return render(request, 'show_despesa.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_salario_view(request, salario_id):
    data = Salario.objects.get(salario_id=salario_id)
    head = [field.name for field in Salario._meta.fields]
    data_dict = {head[i]: data.__dict__[head[i]] for i in range(1, len(head))}
    return render(request, 'show_salario.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_filiacao_view(request, filiacao_id):
    data = Filiacao.objects.get(filiacao_id=filiacao_id)
    head = [field.name for field in Filiacao._meta.fields]
    data_dict = {head[i]: data.__dict__[head[i]] for i in range(1, len(head))}
    return render(request, 'show_filiacao.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

