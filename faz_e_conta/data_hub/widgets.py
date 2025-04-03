from django import forms

def Aluno_widget():
    # Adiciona atributos aos campos do formulário
    widgets = {
        'data_admissao': forms.DateInput(attrs={'type': 'date'}),
        'data_ultima_renovacao': forms.DateInput(attrs={'type': 'date'}),
        'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        'data_validade': forms.DateInput(attrs={'type': 'date'}),
    }
    return widgets

def Responsavel_educativo_widget():
    widgets = {
        'nome': forms.TextInput(attrs={'placeholder': 'Nome do responsável'}),
        'telefone': forms.TextInput(attrs={'type': 'tel', 'placeholder': 'Telefone'}),
        'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
    }
    return widgets

def Aluno_saida_widget():
    widgets = {
        'data_saida': forms.DateInput(attrs={'type': 'date'}),
        'motivo_saida': forms.Textarea(attrs={'placeholder': 'Motivo da saída'}),
    }
    return widgets

def Vacinacao_widget():
    widgets = {
        'data_vacinacao': forms.DateInput(attrs={'type': 'date'}),
        'tipo_vacina': forms.TextInput(attrs={'placeholder': 'Tipo de vacina'}),
        'dose': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Dose'}),
    }
    return widgets

def Despesa_widget():
    widgets = {
        'descricao': forms.TextInput(attrs={'placeholder': 'Descrição da despesa'}),
        'valor': forms.NumberInput(attrs={'placeholder': 'Valor'}),
        'data_despesa': forms.DateInput(attrs={'type': 'date'}),
    }
    return widgets

def Salario_widget():
    widgets = {
        'funcionario': forms.TextInput(attrs={'placeholder': 'Nome do funcionário'}),
        'valor_salario': forms.NumberInput(attrs={'placeholder': 'Valor do salário'}),
        'data_pagamento': forms.DateInput(attrs={'type': 'date'}),
    }
    return widgets

def Filiacao_widget():
    widgets = {
        'nome_pai': forms.TextInput(attrs={'placeholder': 'Nome do pai'}),
        'nome_mae': forms.TextInput(attrs={'placeholder': 'Nome da mãe'}),
        'responsavel': forms.TextInput(attrs={'placeholder': 'Responsável'}),
    }
    return widgets

def Despesa_fixa_widget():
    widgets = {
        'produto': forms.TextInput(attrs={'placeholder': 'Produto'}),
        'valor': forms.NumberInput(attrs={'placeholder': 'Valor'}),
        'data': forms.DateInput(attrs={'type': 'date'}),
        'fatura': forms.NumberInput(attrs={'placeholder': 'Fatura'}),
        'pagamento': forms.TextInput(attrs={'placeholder': 'Pagamento'}),
    }
    return widgets

def Despesas_variavel_widget():
    widgets = {
        'produto': forms.TextInput(attrs={'placeholder': 'Produto'}),
        'valor': forms.NumberInput(attrs={'placeholder': 'Valor'}),
        'data': forms.DateInput(attrs={'type': 'date'}),
        'fatura': forms.NumberInput(attrs={'placeholder': 'Fatura'}),
        'pagamento': forms.TextInput(attrs={'placeholder': 'Pagamento'}),
    }
    return widgets

def Link_filiacao_widget():
    widgets = {
        'type': forms.TextInput(attrs={'placeholder': 'Tipo de ligação'}),
    }
    return widgets

def Sala_widget():
    widgets = {
        'sala_nome': forms.TextInput(attrs={'placeholder': 'Nome da sala'}),
        'sala_local': forms.TextInput(attrs={'placeholder': 'Local da sala'}),
        'sala_valencia': forms.TextInput(attrs={'placeholder': 'Valência da sala'}),
    }
    return widgets

def Mensalidade_aluno_widget():
    widgets = {
        'data_pagamento': forms.DateInput(attrs={'type': 'date'}),
        'valor': forms.NumberInput(attrs={'placeholder': 'Valor'}),
    }
    return widgets

def Aluno_financas_widget():
    widgets = {
        'data_pagamento': forms.DateInput(attrs={'type': 'date'}),
        'valor': forms.NumberInput(attrs={'placeholder': 'Valor'}),
    }
    return widgets

def Aluno_finacas_calc_widget():
    widgets = {
        'data_pagamento': forms.DateInput(attrs={'type': 'date'}),
        'valor': forms.NumberInput(attrs={'placeholder': 'Valor'}),
    }
    return widgets

def Funcionario_widget():
    widgets = {
        'nome': forms.TextInput(attrs={'placeholder': 'Nome do funcionário'}),
        'telefone': forms.TextInput(attrs={'type': 'tel', 'placeholder': 'Telefone'}),
        'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        'data_admissao': forms.DateInput(attrs={'type': 'date'}),
        'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
    }
    return widgets
    