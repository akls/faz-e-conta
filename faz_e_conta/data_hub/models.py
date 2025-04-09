from django.db import models
import datetime
import django.utils as du

class Aluno(models.Model):
    class Meta:
        db_table = 'aluno'
    aluno_id = models.AutoField(primary_key=True)
    nome_proprio = models.CharField(max_length=100, default='')
    apelido = models.CharField(max_length=250, default='')
    archive_flag = models.BooleanField(default=False)
    processo = models.CharField(max_length=150, null=True, blank=True)
    data_admissao = models.DateTimeField()
    data_ultima_renovacao = models.DateTimeField(null=True, blank=True)
    data_nascimento = models.DateTimeField()
    documento = models.CharField(max_length=250, default='')
    numero_documento = models.CharField(max_length=100, default='')
    data_validade = models.DateTimeField()
    niss = models.IntegerField(null=True, blank=True)
    nif = models.IntegerField(null=True, blank=True)
    morada = models.CharField(max_length=150, default='')
    codigo_postal = models.CharField(max_length=150, default='')
    concelho = models.CharField(max_length=150, default='')
    fregesia = models.CharField(max_length=150, null=True, blank=True)
    escolaridade_anterior = models.CharField(max_length=150, null=True, blank=True)
    motivo_admissao = models.CharField(max_length=150, null=True, blank=True)
    cuidados_especias = models.CharField(max_length=150, null=True, blank=True)
    sala_id = models.ForeignKey(to='Sala', on_delete=models.CASCADE, db_column='sala_id')

    def __str__(self):
        return f"{self.nome_proprio} {self. apelido}, Aluno Id: {self.aluno_id}"

class ResponsavelEducativo(models.Model):
    class Meta:
        db_table = 'responsavel_educativo'
    responsavel_educativo_id = models.AutoField(primary_key=True)
    nome_proprio = models.CharField(max_length=100, default='')
    apelido = models.CharField(max_length=250, default='')
    data_nascimento = models.DateField(default= du.timezone.now)
    documento = models.CharField(max_length=150, default='')
    numero_documento = models.IntegerField()
    data_validade = models.DateField(default= du.timezone.now)
    niss = models.IntegerField(null=True, blank=True)
    nif = models.IntegerField(null=True, blank=True)
    morada = models.CharField(max_length=250, default='')
    codigo_postal = models.CharField(max_length=100, default='')
    concelho = models.CharField(max_length=150, default='')
    fregesia = models.CharField(max_length=150, default='')
    telefone = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    profissao = models.CharField(max_length=150, null=True, blank=True)
    morada_emprego = models.CharField(max_length=150, null=True, blank=True)
    horario_trabalho = models.TimeField(null=True, blank=True)
    aluno_id = models.ForeignKey(to='Aluno', on_delete=models.CASCADE, db_column='aluno_id')

    def __str__(self):
        return f"{self.nome_proprio} {self. apelido}, Responsavel Educativo Id: {self.responsavel_educativo_id}"

class AlunoSaida(models.Model):
    class Meta:
        db_table = 'aluno_saida'
    aluno_saida_id = models.AutoField(primary_key=True)
    aluno_id = models.ForeignKey(to='Aluno', on_delete=models.CASCADE, db_column='aluno_id')
    hora_entrada = models.DateTimeField(null=True, blank=True)
    hora_saida = models.DateTimeField(null=True, blank=True)
    autorizacao_sair = models.CharField(max_length=250, null=True, blank=True)
    valencia = models.ForeignKey(to='Alunofinacascalc', on_delete=models.CASCADE, db_column='valencia')

    def __str__(self):
        return f"{self.aluno_id} {self. hora_entrada}, Aluno Saida Id: {self.aluno_saida_id}"

class Vacinacao(models.Model):
    class Meta:
        db_table = 'vacinacao'
    vacinacao_id = models.AutoField(primary_key=True)
    aluno_id = models.ForeignKey(to='Aluno', on_delete=models.CASCADE, db_column='aluno_id')
    dose_id = models.ForeignKey(to='Dose', on_delete=models.CASCADE, db_column='dose_id')
    data_vacina = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.aluno_id} {self. dose_id}, Vacinacao Id: {self.vacinacao_id}"

class DespesaFixa(models.Model):
    class Meta:
        db_table = 'despesa_fixa'
    despesa_fixa_id = models.AutoField(primary_key=True)
    produto = models.CharField(max_length=250, default='')
    valor = models.FloatField()
    data = models.DateTimeField()
    fatura = models.IntegerField()
    pagamento = models.CharField(max_length=250, default='')

    def __str__(self):
        return f"{self.produto} {self. valor}, Despesa Fixa Id: {self.despesa_fixa_id}"

class DespesasVariavel(models.Model):
    class Meta:
        db_table = 'despesas_variavel'
    despesas_variavel_id = models.AutoField(primary_key=True)
    produto = models.CharField(max_length=250, default='')
    valor = models.FloatField()
    data = models.DateTimeField()
    fatura = models.IntegerField()
    pagamento = models.CharField(max_length=250, default='')

    def __str__(self):
        return f"{self.produto} {self. valor}, Despesas Variavel Id: {self.despesas_variavel_id}"

class Salario(models.Model):
    class Meta:
        db_table = 'salario'
    salario_id = models.AutoField(primary_key=True)
    valor = models.FloatField()
    descricao = models.CharField(max_length=250, null=True, blank=True)
    data_pagamento = models.DateField(default= du.timezone.now, null=True, blank=True)
    subsidio_tipo = models.CharField(max_length=20, default='')
    subsidio_valor = models.FloatField()

    def __str__(self):
        return f"{self.valor} {self. descricao}, Salario Id: {self.salario_id}"

class LinkFiliacao(models.Model):
    class Meta:
        db_table = 'link_filiacao'
    aluno_id = models.ForeignKey(to='Aluno', on_delete=models.CASCADE, db_column='aluno_id')
    responsavel_educativo_id = models.ForeignKey(to='Responsaveleducativo', on_delete=models.CASCADE, db_column='responsavel_educativo_id')
    type = models.CharField(max_length=100, default='')
    encarr_educacao = models.BooleanField(default=False, null=True, blank=True)
    link_filiacao_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.responsavel_educativo_id} {self. type}, Aluno Id: {self.aluno_id}"

class Sala(models.Model):
    class Meta:
        db_table = 'sala'
    sala_id = models.AutoField(primary_key=True)
    sala_nome = models.CharField(max_length=255, default='')
    sala_local = models.CharField(max_length=255, null=True, blank=True)
    sala_valencia = models.CharField(max_length=255, default='')
    funcionario_id = models.ForeignKey(to='Funcionario', on_delete=models.CASCADE, db_column='funcionario_id', null=True, blank=True)

    def __str__(self):
        return f"{self.sala_nome} {self. sala_local}, Sala Id: {self.sala_id}"

class MensalidadeAluno(models.Model):
    class Meta:
        db_table = 'mensalidade_aluno'
    mensalidade_aluno_id = models.AutoField(primary_key=True)
    aluno_id = models.ForeignKey(to='Aluno', on_delete=models.CASCADE, db_column='aluno_id')
    aluno_financas_id = models.ForeignKey(to='Alunofinancas', on_delete=models.CASCADE, db_column='aluno_financas_id')
    periodo_inicio = models.DateField(default= du.timezone.now)
    periodo_fim = models.DateField(default= du.timezone.now, null=True, blank=True)
    mensalidade_calc = models.IntegerField(null=True, blank=True)
    mensalidade_retific = models.IntegerField(null=True, blank=True)
    mensalidade_paga = models.IntegerField(null=True, blank=True)
    data_pagamento = models.DateField(default= du.timezone.now, null=True, blank=True)
    modo_pagamento = models.CharField(max_length=255, null=True, blank=True)
    acordo = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.aluno_id} {self. aluno_financas_id}, Mensalidade Aluno Id: {self.mensalidade_aluno_id}"

class AlunoFinancas(models.Model):
    class Meta:
        db_table = 'aluno_financas'
    aluno_financas_id = models.AutoField(primary_key=True)
    ano_letivo = models.CharField(max_length=255, default='')
    aluno_id = models.ForeignKey(to='Aluno', on_delete=models.CASCADE, db_column='aluno_id')
    data = models.DateTimeField(null=True, blank=True)
    agregado = models.IntegerField()
    rendim_líquido = models.IntegerField()
    despesa_anual = models.IntegerField()
    irs = models.CharField(max_length=255, default='')
    tax_soc = models.CharField(max_length=255, default='')
    tax_impos = models.CharField(max_length=255, null=True, blank=True)
    renda = models.IntegerField(null=True, blank=True)
    med_transp = models.CharField(max_length=255, null=True, blank=True)
    medicacao = models.CharField(max_length=255, null=True, blank=True)
    outros = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.ano_letivo} {self. aluno_id}, Aluno Financas Id: {self.aluno_financas_id}"

class AlunoFinacasCalc(models.Model):
    class Meta:
        db_table = 'aluno_finacas_calc'
    sala_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, default='')
    local = models.CharField(max_length=255, null=True, blank=True)
    valencia = models.CharField(max_length=255, default='')
    funcionario_id = models.ForeignKey(to='Funcionario', on_delete=models.CASCADE, db_column='funcionario_id', null=True, blank=True)

    def __str__(self):
        return f"{self.nome} {self. local}, Sala Id: {self.sala_id}"

class Funcionario(models.Model):
    class Meta:
        db_table = 'funcionario'
    funcionario_id = models.AutoField(primary_key=True)
    nome_proprio = models.CharField(max_length=100, default='')
    apelido = models.CharField(max_length=100, default='')
    data_nascimento = models.DateField(default= du.timezone.now)
    tipo_documento_identificacao = models.CharField(max_length=50, null=True, blank=True)
    numero_documento_identificacao = models.CharField(max_length=50, default='')
    data_validade = models.DateField(default= du.timezone.now, null=True, blank=True)
    niss = models.IntegerField()
    nif = models.IntegerField()
    morada = models.CharField(max_length=255, default='')
    codigo_postal = models.CharField(max_length=255, default='')
    concelho = models.CharField(max_length=255, null=True, blank=True)
    freguesia_residencia = models.CharField(max_length=255, null=True, blank=True)
    contacto_telefonico = models.CharField(max_length=255, default='')
    email = models.EmailField()
    funcao = models.CharField(max_length=255, default='')
    salario = models.ForeignKey(to='Salario', on_delete=models.CASCADE, db_column='salario', null=True, blank=True)
    escalao_profissional = models.CharField(max_length=255, null=True, blank=True)
    ativo = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.nome_proprio} {self. apelido}, Funcionario Id: {self.funcionario_id}"

class ComparticipacaoMensalSs(models.Model):
    class Meta:
        db_table = 'comparticipacao_mensal_ss'
    comparticipacao_mensal_ss_id = models.AutoField(primary_key=True)
    aluno_id = models.ForeignKey(to='Aluno', on_delete=models.CASCADE, db_column='aluno_id')
    aluno_financas_id = models.ForeignKey(to='Alunofinancas', on_delete=models.CASCADE, db_column='aluno_financas_id')
    periodo_inicio = models.DateField(default= du.timezone.now)
    periodo_fim = models.DateField(default= du.timezone.now, null=True, blank=True)
    mensalidade_valor = models.IntegerField()
    mensalidade_paga = models.IntegerField(null=True, blank=True)
    data_pagamento = models.DateField(default= du.timezone.now, null=True, blank=True)
    modo_pagamento = models.CharField(max_length=255, null=True, blank=True)
    programa_ss = models.CharField(max_length=255, null=True, blank=True)
    acordo = models.ForeignKey(to='Acordo', on_delete=models.CASCADE, db_column='acordo', null=True, blank=True)

    def __str__(self):
        return f"{self.aluno_id} {self. aluno_financas_id}, Comparticipacao Mensal Ss Id: {self.comparticipacao_mensal_ss_id}"

class Vacina(models.Model):
    class Meta:
        db_table = 'vacina'
    vacina_id = models.AutoField(primary_key=True)
    vacina_name = models.CharField(max_length=250, default='')
    plano_vacina = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.vacina_name} {self. plano_vacina}, Vacina Id: {self.vacina_id}"

class Dose(models.Model):
    class Meta:
        db_table = 'dose'
    idade = models.IntegerField()
    obrigatoria = models.BooleanField(default=False)
    periodo_recomendado = models.IntegerField()
    dose = models.IntegerField()
    vacina_id = models.ForeignKey(to='Vacina', on_delete=models.CASCADE, db_column='vacina_id')
    dose_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.obrigatoria} {self. periodo_recomendado}, Idade: {self.idade}"

class Divida(models.Model):
    class Meta:
        db_table = 'divida'
    divida_id = models.AutoField(primary_key=True)
    aluno_id = models.ForeignKey(to='Aluno', on_delete=models.CASCADE, db_column='aluno_id')
    valor_pagar = models.IntegerField()
    valor_pago = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.aluno_id} {self. valor_pagar}, Divida Id: {self.divida_id}"

class Acordo(models.Model):
    class Meta:
        db_table = 'acordo'
    acordo_id = models.AutoField(primary_key=True)
    responsavel_educativo_id = models.ForeignKey(to='Responsaveleducativo', on_delete=models.CASCADE, db_column='responsavel_educativo_id')
    divida_id = models.ForeignKey(to='Divida', on_delete=models.CASCADE, db_column='divida_id')

    def __str__(self):
        return f"{self.responsavel_educativo_id} {self. divida_id}, Acordo Id: {self.acordo_id}"

