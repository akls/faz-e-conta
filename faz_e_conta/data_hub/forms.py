from django import forms
from .models import *
from .widgets import *

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['aluno_id', 'nome_proprio', 'apelido', 'archive_flag', 'processo', 'data_admissao', 'data_ultima_renovacao', 'data_nascimento', 'documento', 'numero_documento', 'data_validade', 'niss', 'nif', 'morada', 'codigo_postal', 'concelho', 'fregesia', 'escolaridade_anterior', 'motivo_admissao', 'cuidados_especias', 'sala_id']

        # Adiciona atributos aos campos do formulário
        widgets = Aluno_widget()

class Responsavel_educativoForm(forms.ModelForm):
    class Meta:
        model = ResponsavelEducativo
        fields = ['responsavel_educativo_id', 'nome_proprio', 'apelido', 'data_nascimento', 'documento', 'numero_documento', 'data_validade', 'niss', 'nif', 'morada', 'codigo_postal', 'concelho', 'fregesia', 'telefone', 'email', 'profissao', 'morada_emprego', 'horario_trabalho', 'aluno_id']

        # Adiciona atributos aos campos do formulário
        widgets = Responsavel_educativo_widget()

class Aluno_saidaForm(forms.ModelForm):
    class Meta:
        model = AlunoSaida
        fields = ['saida_id', 'aluno_id', 'hora_entrada', 'hora_saida', 'autorizacao_sair', 'valencia']

        # Adiciona atributos aos campos do formulário
        widgets = Aluno_saida_widget()

class VacinacaoForm(forms.ModelForm):
    class Meta:
        model = Vacinacao
        fields = ['vac_id', 'aluno_id', 'vacina_name', 'data_vacina', 'plano_vacina']

        # Adiciona atributos aos campos do formulário
        widgets = Vacinacao_widget()

class Despesa_fixaForm(forms.ModelForm):
    class Meta:
        model = DespesaFixa
        fields = ['despfix_id', 'produto', 'valor', 'data', 'fatura', 'pagamento']

        # Adiciona atributos aos campos do formulário
        widgets = Despesa_fixa_widget()

class Despesas_variavelForm(forms.ModelForm):
    class Meta:
        model = DespesasVariavel
        fields = ['despvar_id', 'produto', 'valor', 'data', 'fatura', 'pagamento']

        # Adiciona atributos aos campos do formulário
        widgets = Despesas_variavel_widget()

class SalarioForm(forms.ModelForm):
    class Meta:
        model = Salario
        fields = ['salario_id', 'valor', 'descricao', 'data_pagamento', 'subsidio_tipo', 'subsidio_valor']

        # Adiciona atributos aos campos do formulário
        widgets = Salario_widget()

class Link_filiacaoForm(forms.ModelForm):
    class Meta:
        model = LinkFiliacao
        fields = ['aluno_id', 're_id', 'type', 'encarr_educacao']

        # Adiciona atributos aos campos do formulário
        widgets = Link_filiacao_widget()

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['sala_id', 'sala_nome', 'sala_local', 'sala_valencia', 'func_id']

        # Adiciona atributos aos campos do formulário
        widgets = Sala_widget()

class Mensalidade_alunoForm(forms.ModelForm):
    class Meta:
        model = MensalidadeAluno
        fields = ['ma_id', 'aluno_id', 'ano_letivo', 'periodo_inicio', 'periodo_fim', 'mensalidade_calc', 'mensalidade_retific', 'mensalidade_paga', 'data_pagamento', 'modo_pagamento', 'acordo']

        # Adiciona atributos aos campos do formulário
        widgets = Mensalidade_aluno_widget()

class Aluno_financasForm(forms.ModelForm):
    class Meta:
        model = AlunoFinancas
        fields = ['af_id', 'ano_letivo', 'aluno_id', 'data', 'agregado', 'rendim_líquido', 'despesa_anual', 'irs', 'tax_soc', 'tax_impos', 'renda', 'med_transp', 'medicacao', 'outros']

        # Adiciona atributos aos campos do formulário
        widgets = Aluno_financas_widget()

class Aluno_finacas_calcForm(forms.ModelForm):
    class Meta:
        model = AlunoFinacasCalc
        fields = ['sala_id', 'nome', 'local', 'valencia', 'func_id']

        # Adiciona atributos aos campos do formulário
        widgets = Aluno_finacas_calc_widget()

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['func_id', 'nome_proprio', 'apelido', 'data_nascimento', 'tipo_documento_identificacao', 'numero_documento_identificacao', 'data_validade', 'niss', 'nif', 'morada', 'codigo_postal', 'concelho', 'freguesia_residencia', 'contacto_telefonico', 'email', 'funcao', 'salario', 'escalao_profissional', 'ativo']

        # Adiciona atributos aos campos do formulário
        widgets = Funcionario_widget()

