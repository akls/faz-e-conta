from django import forms

def Aluno_widget():
    widgets = {
        'data_admissao': forms.DateInput(attrs={'type': 'date'}),
        'data_ultima_renovacao': forms.DateInput(attrs={'type': 'date'}),
        'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        'data_validade': forms.DateInput(attrs={'type': 'date'}),
    }
    return widgets

def Responsavel_educativo_widget():
    widgets = {
        'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        'data_validade': forms.DateInput(attrs={'type': 'date'}),
    }
    return widgets

def Aluno_saida_widget():
    widgets = {
        'hora_entrada': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        'hora_saida': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    }
    return widgets

def Vacinacao_widget():
    widgets = {
        'data_vacina': forms.DateInput(attrs={'type': 'date'}),
    }
    return widgets

def Salario_widget():
    widgets = {
        'data_pagamento': forms.DateInput(attrs={'type': 'date'}),
    }
    return widgets

def Filiacao_widget():
    widgets = {
        'encarr_educacao': forms.CheckboxInput(),
    }
    return widgets

def Mensalidade_aluno_widget():
    widgets = {
        'periodo_inicio': forms.DateInput(attrs={'type': 'date'}),
        'periodo_fim': forms.DateInput(attrs={'type': 'date'}),
        'data_pagamento': forms.DateInput(attrs={'type': 'date'}),
    }
    return widgets

def Aluno_financas_widget():
    widgets = {
        'data': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    }
    return widgets

def Funcionario_widget():
    widgets = {
        'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        'data_validade': forms.DateInput(attrs={'type': 'date'}),
    }
    return widgets

def Sala_widget():
    widgets = {
        'sala_local': forms.TextInput(attrs={'type': 'text'}),
    }
    return widgets

def Link_filiacao_widget():
    widgets = {
        'encarr_educacao': forms.CheckboxInput(),
    }
    return widgets

def Aluno_finacas_calc_widget():
    widgets = {
        'local': forms.TextInput(attrs={'type': 'text'}),
    }
    return widgets

def Despesa_fixa_widget():
    widgets = {
        'data': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    }
    return widgets

def Despesas_variavel_widget():
    widgets = {
        'data': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    }
    return widgets
