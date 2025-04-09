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
    head = [field.name for field in Aluno.objects.model._meta.fields]

    data_dict = {}
    for field in head:
        data_dict[field] = getattr(data, field, None)
    return render(request, 'show_aluno.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_responsavel_educativo_view(request, responsavel_educativo_id):
    try:
        data = ResponsavelEducativo.objects.get(responsavel_educativo_id=responsavel_educativo_id)  # Verifique se 'id' é o nome correto do campo
    except ResponsavelEducativo.DoesNotExist:
        return HttpResponse(f'<h1>Responsavel Educativo with id= {responsavel_educativo_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name for field in ResponsavelEducativo.objects.model._meta.fields]

    data_dict = {}
    for field in head:
        data_dict[field] = getattr(data, field, None)
    return render(request, 'show_responsavel_educativo.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_aluno_saida_view(request, aluno_saida_id):
    try:
        data = AlunoSaida.objects.get(aluno_saida_id=aluno_saida_id)  # Verifique se 'id' é o nome correto do campo
    except AlunoSaida.DoesNotExist:
        return HttpResponse(f'<h1>Aluno Saida with id= {aluno_saida_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name for field in AlunoSaida.objects.model._meta.fields]

    data_dict = {}
    for field in head:
        data_dict[field] = getattr(data, field, None)
    return render(request, 'show_aluno_saida.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_vacinacao_view(request, vacinacao_id):
    try:
        data = Vacinacao.objects.get(vacinacao_id=vacinacao_id)  # Verifique se 'id' é o nome correto do campo
    except Vacinacao.DoesNotExist:
        return HttpResponse(f'<h1>Vacinacao with id= {vacinacao_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name for field in Vacinacao.objects.model._meta.fields]

    data_dict = {}
    for field in head:
        data_dict[field] = getattr(data, field, None)
    return render(request, 'show_vacinacao.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_despesa_fixa_view(request, despesa_fixa_id):
    try:
        data = DespesaFixa.objects.get(despesa_fixa_id=despesa_fixa_id)  # Verifique se 'id' é o nome correto do campo
    except DespesaFixa.DoesNotExist:
        return HttpResponse(f'<h1>Despesa Fixa with id= {despesa_fixa_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name for field in DespesaFixa.objects.model._meta.fields]

    data_dict = {}
    for field in head:
        data_dict[field] = getattr(data, field, None)
    return render(request, 'show_despesa_fixa.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_despesas_variavel_view(request, despesas_variavel_id):
    try:
        data = DespesasVariavel.objects.get(despesas_variavel_id=despesas_variavel_id)  # Verifique se 'id' é o nome correto do campo
    except DespesasVariavel.DoesNotExist:
        return HttpResponse(f'<h1>Despesas Variavel with id= {despesas_variavel_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name for field in DespesasVariavel.objects.model._meta.fields]

    data_dict = {}
    for field in head:
        data_dict[field] = getattr(data, field, None)
    return render(request, 'show_despesas_variavel.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_salario_view(request, salario_id):
    try:
        data = Salario.objects.get(salario_id=salario_id)  # Verifique se 'id' é o nome correto do campo
    except Salario.DoesNotExist:
        return HttpResponse(f'<h1>Salario with id= {salario_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name for field in Salario.objects.model._meta.fields]

    data_dict = {}
    for field in head:
        data_dict[field] = getattr(data, field, None)
    return render(request, 'show_salario.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_link_filiacao_view(request, link_filiacao_id):
    try:
        data = LinkFiliacao.objects.get(link_filiacao_id=link_filiacao_id)  # Verifique se 'id' é o nome correto do campo
    except LinkFiliacao.DoesNotExist:
        return HttpResponse(f'<h1>Link Filiacao with id= {link_filiacao_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name for field in LinkFiliacao.objects.model._meta.fields]

    data_dict = {}
    for field in head:
        data_dict[field] = getattr(data, field, None)
    return render(request, 'show_link_filiacao.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_sala_view(request, sala_id):
    try:
        data = Sala.objects.get(sala_id=sala_id)  # Verifique se 'id' é o nome correto do campo
    except Sala.DoesNotExist:
        return HttpResponse(f'<h1>Sala with id= {sala_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name for field in Sala.objects.model._meta.fields]

    data_dict = {}
    for field in head:
        data_dict[field] = getattr(data, field, None)
    return render(request, 'show_sala.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_mensalidade_aluno_view(request, mensalidade_aluno_id):
    try:
        data = MensalidadeAluno.objects.get(mensalidade_aluno_id=mensalidade_aluno_id)  # Verifique se 'id' é o nome correto do campo
    except MensalidadeAluno.DoesNotExist:
        return HttpResponse(f'<h1>Mensalidade Aluno with id= {mensalidade_aluno_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name for field in MensalidadeAluno.objects.model._meta.fields]

    data_dict = {}
    for field in head:
        data_dict[field] = getattr(data, field, None)
    return render(request, 'show_mensalidade_aluno.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_aluno_financas_view(request, aluno_financas_id):
    try:
        data = AlunoFinancas.objects.get(aluno_financas_id=aluno_financas_id)  # Verifique se 'id' é o nome correto do campo
    except AlunoFinancas.DoesNotExist:
        return HttpResponse(f'<h1>Aluno Financas with id= {aluno_financas_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name for field in AlunoFinancas.objects.model._meta.fields]

    data_dict = {}
    for field in head:
        data_dict[field] = getattr(data, field, None)
    return render(request, 'show_aluno_financas.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_aluno_finacas_calc_view(request, aluno_finacas_calc_id):
    try:
        data = AlunoFinacasCalc.objects.get(aluno_finacas_calc_id=aluno_finacas_calc_id)  # Verifique se 'id' é o nome correto do campo
    except AlunoFinacasCalc.DoesNotExist:
        return HttpResponse(f'<h1>Aluno Finacas Calc with id= {aluno_finacas_calc_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name for field in AlunoFinacasCalc.objects.model._meta.fields]

    data_dict = {}
    for field in head:
        data_dict[field] = getattr(data, field, None)
    return render(request, 'show_aluno_finacas_calc.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_funcionario_view(request, funcionario_id):
    try:
        data = Funcionario.objects.get(funcionario_id=funcionario_id)  # Verifique se 'id' é o nome correto do campo
    except Funcionario.DoesNotExist:
        return HttpResponse(f'<h1>Funcionario with id= {funcionario_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name for field in Funcionario.objects.model._meta.fields]

    data_dict = {}
    for field in head:
        data_dict[field] = getattr(data, field, None)
    return render(request, 'show_funcionario.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_comparticipacao_mensal_ss_view(request, comparticipacao_mensal_ss_id):
    try:
        data = ComparticipacaoMensalSs.objects.get(comparticipacao_mensal_ss_id=comparticipacao_mensal_ss_id)  # Verifique se 'id' é o nome correto do campo
    except ComparticipacaoMensalSs.DoesNotExist:
        return HttpResponse(f'<h1>Comparticipacao Mensal Ss with id= {comparticipacao_mensal_ss_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name for field in ComparticipacaoMensalSs.objects.model._meta.fields]

    data_dict = {}
    for field in head:
        data_dict[field] = getattr(data, field, None)
    return render(request, 'show_comparticipacao_mensal_ss.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_vacina_view(request, vacina_id):
    try:
        data = Vacina.objects.get(vacina_id=vacina_id)  # Verifique se 'id' é o nome correto do campo
    except Vacina.DoesNotExist:
        return HttpResponse(f'<h1>Vacina with id= {vacina_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name for field in Vacina.objects.model._meta.fields]

    data_dict = {}
    for field in head:
        data_dict[field] = getattr(data, field, None)
    return render(request, 'show_vacina.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_dose_view(request, dose_id):
    try:
        data = Dose.objects.get(dose_id=dose_id)  # Verifique se 'id' é o nome correto do campo
    except Dose.DoesNotExist:
        return HttpResponse(f'<h1>Dose with id= {dose_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name for field in Dose.objects.model._meta.fields]

    data_dict = {}
    for field in head:
        data_dict[field] = getattr(data, field, None)
    return render(request, 'show_dose.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_divida_view(request, divida_id):
    try:
        data = Divida.objects.get(divida_id=divida_id)  # Verifique se 'id' é o nome correto do campo
    except Divida.DoesNotExist:
        return HttpResponse(f'<h1>Divida with id= {divida_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name for field in Divida.objects.model._meta.fields]

    data_dict = {}
    for field in head:
        data_dict[field] = getattr(data, field, None)
    return render(request, 'show_divida.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

def show_acordo_view(request, acordo_id):
    try:
        data = Acordo.objects.get(acordo_id=acordo_id)  # Verifique se 'id' é o nome correto do campo
    except Acordo.DoesNotExist:
        return HttpResponse(f'<h1>Acordo with id= {acordo_id} not found</h1><a href="/">Voltar para o índice</a>')
    head = [field.name for field in Acordo.objects.model._meta.fields]

    data_dict = {}
    for field in head:
        data_dict[field] = getattr(data, field, None)
    return render(request, 'show_acordo.html', {'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]})

