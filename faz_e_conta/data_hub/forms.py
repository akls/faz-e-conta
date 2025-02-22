from django import forms
from .models import Aluno, Responsavel_educativo, Aluno_saida, Vacinacao, Despesa, Salario, Filiacao

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['aluno_id', 'nome_proprio', 'apelido', 'processo', 'data_admissao', 'data_ultima_renovacao', 'data_nascimento', 'documento', 'numero_documento', 'data_validade', 'niss', 'nif', 'morada', 'codigo_postal', 'concelho', 'fregesia', 'escolaridade_anterior', 'motivo_admissao', 'cuidados_especias']

class Responsavel_educativoForm(forms.ModelForm):
    class Meta:
        model = Responsavel_educativo
        fields = ['respon_id', 'nome_proprio', 'apelido', 'data_nascimento', 'documento', 'numero_documento', 'data_validade', 'niss', 'nif', 'morada', 'codigo_postal', 'concelho', 'fregesia', 'telefone', 'email', 'profissao', 'morada_emprego', 'horario_trabalho', 'aluno_id']

class Aluno_saidaForm(forms.ModelForm):
    class Meta:
        model = Aluno_saida
        fields = ['saida_id', 'aluno_id', 'hora_entrada', 'hora_saida', 'autorizacao_sair', 'escolaridade']

class VacinacaoForm(forms.ModelForm):
    class Meta:
        model = Vacinacao
        fields = ['vac_id', 'aluno_id', 'vacina_name', 'data_vacina', 'plano_vacina']

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['despesa_id', 'categoria', 'valor', 'descricao', 'data']

class SalarioForm(forms.ModelForm):
    class Meta:
        model = Salario
        fields = ['salario_id', 'funcionario_id', 'valor', 'descricao', 'data_pagamento', 'subsidio_tipo', 'subsidio_valor']

class FiliacaoForm(forms.ModelForm):
    class Meta:
        model = Filiacao
        fields = ['filiacao_id', 'aluno_id', 'respon_id', 'filiacao_responsavel']

