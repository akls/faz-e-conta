from django import forms
from .models import *
from .widgets import *

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['aluno_id', 'nome_proprio', 'apelido', 'archive_flag', 'processo', 'data_admissao', 'data_ultima_renovacao', 'data_nascimento', 'documento', 'numero_documento', 'data_validade', 'niss', 'nif', 'morada', 'codigo_postal', 'concelho', 'fregesia', 'escolaridade_anterior', 'motivo_admissao', 'cuidados_especias', 'sala_id', 'responsaveis_educativos_ids']


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