from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Aluno, Responsavel_educativo, Aluno_saida, Vacinacao, Despesa, Salario, Filiacao
from .forms import AlunoForm, Responsavel_educativoForm, Aluno_saidaForm, VacinacaoForm, DespesaForm, SalarioForm, FiliacaoForm

def insert_aluno_view(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('aluno_view'))
    else:
        form = AlunoForm()
    return render(request, 'insert_aluno.html', {'form': form})

def insert_responsavel_educativo_view(request):
    if request.method == 'POST':
        form = Responsavel_educativoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('responsavel_educativo_view'))
    else:
        form = Responsavel_educativoForm()
    return render(request, 'insert_responsavel_educativo.html', {'form': form})

def insert_aluno_saida_view(request):
    if request.method == 'POST':
        form = Aluno_saidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('aluno_saida_view'))
    else:
        form = Aluno_saidaForm()
    return render(request, 'insert_aluno_saida.html', {'form': form})

def insert_vacinacao_view(request):
    if request.method == 'POST':
        form = VacinacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('vacinacao_view'))
    else:
        form = VacinacaoForm()
    return render(request, 'insert_vacinacao.html', {'form': form})

def insert_despesa_view(request):
    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('despesa_view'))
    else:
        form = DespesaForm()
    return render(request, 'insert_despesa.html', {'form': form})

def insert_salario_view(request):
    if request.method == 'POST':
        form = SalarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('salario_view'))
    else:
        form = SalarioForm()
    return render(request, 'insert_salario.html', {'form': form})

def insert_filiacao_view(request):
    if request.method == 'POST':
        form = FiliacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('filiacao_view'))
    else:
        form = FiliacaoForm()
    return render(request, 'insert_filiacao.html', {'form': form})

