from django import forms
from django.contrib.auth.models import User

from .models import *
from .widgets import *

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['aluno_id', 'nome_proprio', 'apelido', 'archive_flag', 'processo', 'data_admissao', 'data_ultima_renovacao', 'data_nascimento', 'documento', 'numero_documento', 'data_validade', 'niss', 'nif', 'morada', 'codigo_postal', 'concelho', 'fregesia', 'escolaridade_anterior', 'motivo_admissao', 'cuidados_especias', 'sala_id', 'responsaveis_educativos_ids', "programa_id", "comparticao_ss_custom"]


        # Adiciona atributos aos campos do formulário
        widgets = Aluno_widget()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsaveis_educativos_ids'].queryset = ResponsavelEducativo.objects.order_by('nome_proprio', 'apelido')
        self.fields['sala_id'].queryset = Sala.objects.order_by("sala_nome")

class Responsavel_educativoForm(forms.ModelForm):
    class Meta:
        model = ResponsavelEducativo
        fields = ['responsavel_educativo_id', 'nome_proprio', 'apelido', 'data_nascimento', 'documento', 'numero_documento', 'data_validade', 'niss', 'nif', 'morada', 'codigo_postal', 'concelho', 'fregesia', 'telefone', 'email', 'profissao', 'morada_emprego', 'horario_trabalho']

        # Adiciona atributos aos campos do formulário
        widgets = Responsavel_educativo_widget()

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ["sala_nome", "sala_local", "sala_valencia"]

class FinancasForm(forms.ModelForm):
    class Meta:
        model = AlunoFinancas
        fields = [
            "ano_letivo",
            "aluno_id",
            "data",
            "agregado",
            "rendim_líquido",
            "despesa_anual",
            "irs",
            "tax_soc",
            "tax_impos",
            "renda",
            "med_transp",
            "medicacao",
            "outros",
        ]

class DespesaFixaForm(forms.ModelForm):
    class Meta:
        model = DespesaFixa
        fields = ["produto", "valor", "data", "fatura","pagamento","notas","fornecedor"]
        widgets = Despesa_widget()

class DespesasVariavelForm(forms.ModelForm):
    class Meta:
        model = DespesasVariavel
        fields = ["produto", "valor", "data", "fatura","pagamento","notas","fornecedor"]
        widgets = Despesa_widget()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

class MetodoPagamentoForm(forms.ModelForm):
    class Meta:
        model = MetodoPagamento
        fields = ["metodo"]

class PagamentoMensalidadeForm(forms.ModelForm):
    class Meta:
        model = PagamentoMensalidade
        fields = ["valor", "data", "metodo_pagamento_id"]
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")
        }

class PagamentoComparticaoForm(forms.ModelForm):
    class Meta:
        model = PagamentoComparticao
        fields = ["valor", "data", "metodo_pagamento_id"]
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")
        }