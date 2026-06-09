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
        'nome': forms.TextInput(attrs={'placeholder': 'Nome do responsável'}),
        'telefone': forms.TextInput(attrs={'type': 'tel', 'placeholder': 'Telefone'}),
        'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        'data_validade': forms.DateInput(attrs={'type': 'date'}),
    }
    return widgets

def Despesa_widget():
    widgets = {
        'data': forms.DateInput(attrs={'type': 'date'}),
    }
    return widgets

