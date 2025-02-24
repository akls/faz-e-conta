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
        
    }
    return widgets

def Aluno_saida_widget():
    widgets = {
        
    }
    return widgets

def Vacinacao_widget():
    widgets = {
        
    }
    return widgets

def Despesa_widget():
    widgets = {
        
    }
    return widgets

def Salario_widget():
    widgets = {
        
    }
    return widgets

def Filiacao_widget():
    widgets = {
        
    }
    return widgets

