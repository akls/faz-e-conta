from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import *

def insert_aluno_view(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = AlunoForm()
    return render(request, 'insert_aluno.html', {'form': form})

def insert_responsavel_educativo_view(request):
    if request.method == 'POST':
        form = Responsavel_educativoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = Responsavel_educativoForm()
    return render(request, 'insert_responsavel_educativo.html', {'form': form})

def insert_aluno_saida_view(request):
    if request.method == 'POST':
        form = Aluno_saidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = Aluno_saidaForm()
    return render(request, 'insert_aluno_saida.html', {'form': form})

def insert_vacinacao_view(request):
    if request.method == 'POST':
        form = VacinacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = VacinacaoForm()
    return render(request, 'insert_vacinacao.html', {'form': form})

def insert_despesa_fixa_view(request):
    if request.method == 'POST':
        form = Despesa_fixaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = Despesa_fixaForm()
    return render(request, 'insert_despesa_fixa.html', {'form': form})

def insert_despesas_variavel_view(request):
    if request.method == 'POST':
        form = Despesas_variavelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = Despesas_variavelForm()
    return render(request, 'insert_despesas_variavel.html', {'form': form})

def insert_salario_view(request):
    if request.method == 'POST':
        form = SalarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = SalarioForm()
    return render(request, 'insert_salario.html', {'form': form})

def insert_link_filiacao_view(request):
    if request.method == 'POST':
        form = Link_filiacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = Link_filiacaoForm()
    return render(request, 'insert_link_filiacao.html', {'form': form})

def insert_sala_view(request):
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = SalaForm()
    return render(request, 'insert_sala.html', {'form': form})

def insert_mensalidade_aluno_view(request):
    if request.method == 'POST':
        form = Mensalidade_alunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = Mensalidade_alunoForm()
    return render(request, 'insert_mensalidade_aluno.html', {'form': form})

def insert_aluno_financas_view(request):
    if request.method == 'POST':
        form = Aluno_financasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = Aluno_financasForm()
    return render(request, 'insert_aluno_financas.html', {'form': form})

def insert_aluno_finacas_calc_view(request):
    if request.method == 'POST':
        form = Aluno_finacas_calcForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = Aluno_finacas_calcForm()
    return render(request, 'insert_aluno_finacas_calc.html', {'form': form})

def insert_funcionario_view(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = FuncionarioForm()
    return render(request, 'insert_funcionario.html', {'form': form})

