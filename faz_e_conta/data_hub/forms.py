from django import forms
from .models import *
from .widgets import *

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['aluno_id', 'nome_proprio', 'apelido', 'archive_flag', 'processo', 'data_admissao', 'data_ultima_renovacao', 'data_nascimento', 'documento', 'numero_documento', 'data_validade', 'niss', 'nif', 'morada', 'codigo_postal', 'concelho', 'fregesia', 'escolaridade_anterior', 'motivo_admissao', 'cuidados_especias', 'sala_id']

        # Adiciona atributos aos campos do formulário
        widgets = default_widget()

class Responsavel_educativoForm(forms.ModelForm):
    class Meta:
        model = ResponsavelEducativo
        fields = ['responsavel_educativo_id', 'nome_proprio', 'apelido', 'data_nascimento', 'documento', 'numero_documento', 'data_validade', 'niss', 'nif', 'morada', 'codigo_postal', 'concelho', 'fregesia', 'telefone', 'email', 'profissao', 'morada_emprego', 'horario_trabalho', 'aluno_id']

        # Adiciona atributos aos campos do formulário
        widgets = default_widget()

class Aluno_saidaForm(forms.ModelForm):
    class Meta:
        model = AlunoSaida
        fields = ['aluno_saida_id', 'aluno_id', 'hora_entrada', 'hora_saida', 'autorizacao_sair', 'valencia']

        # Adiciona atributos aos campos do formulário
        widgets = default_widget()

class VacinacaoForm(forms.ModelForm):
    class Meta:
        model = Vacinacao
        fields = ['vacinacao_id', 'aluno_id', 'dose_id', 'data_vacina']

        # Adiciona atributos aos campos do formulário
        widgets = default_widget()

class Despesa_fixaForm(forms.ModelForm):
    class Meta:
        model = DespesaFixa
        fields = ['despesa_fixa_id', 'produto', 'valor', 'data', 'fatura', 'pagamento']

        # Adiciona atributos aos campos do formulário
        widgets = default_widget()

class Despesas_variavelForm(forms.ModelForm):
    class Meta:
        model = DespesasVariavel
        fields = ['despesas_variavel_id', 'produto', 'valor', 'data', 'fatura', 'pagamento']

        # Adiciona atributos aos campos do formulário
        widgets = default_widget()

class SalarioForm(forms.ModelForm):
    class Meta:
        model = Salario
        fields = ['salario_id', 'valor', 'descricao', 'data_pagamento', 'subsidio_tipo', 'subsidio_valor']

        # Adiciona atributos aos campos do formulário
        widgets = default_widget()

class Link_filiacaoForm(forms.ModelForm):
    class Meta:
        model = LinkFiliacao
        fields = ['aluno_id', 'responsavel_educativo_id', 'type', 'encarr_educacao', 'link_filiacao_id']

        # Adiciona atributos aos campos do formulário
        widgets = default_widget()

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['sala_id', 'sala_nome', 'sala_local', 'sala_valencia', 'funcionario_id']

        # Adiciona atributos aos campos do formulário
        widgets = default_widget()

class Mensalidade_alunoForm(forms.ModelForm):
    class Meta:
        model = MensalidadeAluno
        fields = ['mensalidade_aluno_id', 'aluno_id', 'aluno_financas_id', 'periodo_inicio', 'periodo_fim', 'mensalidade_calc', 'mensalidade_retific', 'mensalidade_paga', 'data_pagamento', 'modo_pagamento', 'acordo']

        # Adiciona atributos aos campos do formulário
        widgets = default_widget()

class Aluno_financasForm(forms.ModelForm):
    class Meta:
        model = AlunoFinancas
        fields = ['aluno_financas_id', 'ano_letivo', 'aluno_id', 'data', 'agregado', 'rendim_líquido', 'despesa_anual', 'irs', 'tax_soc', 'tax_impos', 'renda', 'med_transp', 'medicacao', 'outros']

        # Adiciona atributos aos campos do formulário
        widgets = default_widget()

class Aluno_finacas_calcForm(forms.ModelForm):
    class Meta:
        model = AlunoFinacasCalc
        fields = ['sala_id', 'nome', 'local', 'valencia', 'funcionario_id']

        # Adiciona atributos aos campos do formulário
        widgets = default_widget()

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['funcionario_id', 'nome_proprio', 'apelido', 'data_nascimento', 'tipo_documento_identificacao', 'numero_documento_identificacao', 'data_validade', 'niss', 'nif', 'morada', 'codigo_postal', 'concelho', 'freguesia_residencia', 'contacto_telefonico', 'email', 'funcao', 'salario', 'escalao_profissional', 'ativo']

        # Adiciona atributos aos campos do formulário
        widgets = default_widget()

class Comparticipacao_mensal_ssForm(forms.ModelForm):
    class Meta:
        model = ComparticipacaoMensalSs
        fields = ['comparticipacao_mensal_ss_id', 'aluno_id', 'aluno_financas_id', 'periodo_inicio', 'periodo_fim', 'mensalidade_valor', 'mensalidade_paga', 'data_pagamento', 'modo_pagamento', 'programa_ss', 'acordo']

        # Adiciona atributos aos campos do formulário
        widgets = default_widget()

class VacinaForm(forms.ModelForm):
    class Meta:
        model = Vacina
        fields = ['vacina_id', 'vacina_name', 'plano_vacina']

        # Adiciona atributos aos campos do formulário
        widgets = default_widget()

class DoseForm(forms.ModelForm):
    class Meta:
        model = Dose
        fields = ['idade', 'obrigatoria', 'periodo_recomendado', 'dose', 'vacina_id', 'dose_id']

        # Adiciona atributos aos campos do formulário
        widgets = default_widget()

class DividaForm(forms.ModelForm):
    class Meta:
        model = Divida
        fields = ['divida_id', 'aluno_id', 'valor_pagar', 'valor_pago']

        # Adiciona atributos aos campos do formulário
        widgets = default_widget()

class AcordoForm(forms.ModelForm):
    class Meta:
        model = Acordo
        fields = ['acordo_id', 'responsavel_educativo_id', 'divida_id']

        # Adiciona atributos aos campos do formulário
        widgets = default_widget()
