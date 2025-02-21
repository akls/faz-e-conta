from django.db import models

class Aluno(models.Model):
    class Meta:
        db_table = 'aluno'
    aluno_id = models.AutoField(primary_key=True, null=False, blank=False, default = '')
    nome_proprio = models.CharField(max_length=100, null=False, blank=False, default = '')
    apelido = models.CharField(max_length=250, null=False, blank=False, default = '')
    processo = models.CharField(max_length=150, null=True, blank=True)
    data_admissao = models.DateField(null=False, blank=False, default = '')
    data_ultima_renovacao = models.DateField(null=True, blank=True)
    data_nascimento = models.DateField(null=False, blank=False, default = '')
    documento = models.CharField(max_length=250, null=False, blank=False, default = '')
    numero_documento = models.CharField(max_length=100, null=False, blank=False, default = '')
    data_validade = models.DateField(null=False, blank=False, default = '')
    niss = models.IntegerField(null=True, blank=True)
    nif = models.IntegerField(null=True, blank=True)
    morada = models.CharField(max_length=150, null=False, blank=False, default = '')
    codigo_postal = models.CharField(max_length=150, null=False, blank=False, default = '')
    concelho = models.CharField(max_length=150, null=False, blank=False, default = '')
    fregesia = models.CharField(max_length=150, null=True, blank=True)
    escolaridade_anterior = models.CharField(max_length=150, null=True, blank=True)
    motivo_admissao = models.CharField(max_length=150, null=True, blank=True)
    cuidados_especias = models.CharField(max_length=150, null=True, blank=True)

class Responsavel_educativo(models.Model):
    class Meta:
        db_table = 'responsavel_educativo'
    respon_id = models.AutoField(primary_key=True, null=False, blank=False, default = '')
    nome_proprio = models.CharField(max_length=100, null=False, blank=False, default = '')
    apelido = models.CharField(max_length=250, null=False, blank=False, default = '')
    data_nascimento = models.DateField(null=False, blank=False, default = '')
    documento = models.CharField(max_length=150, null=False, blank=False, default = '')
    numero_documento = models.IntegerField(null=False, blank=False, default = '')
    data_validade = models.DateField(null=False, blank=False, default = '')
    niss = models.IntegerField(null=True, blank=True)
    nif = models.IntegerField(null=True, blank=True)
    morada = models.CharField(max_length=250, null=False, blank=False, default = '')
    codigo_postal = models.CharField(max_length=100, null=False, blank=False, default = '')
    concelho = models.CharField(max_length=150, null=False, blank=False, default = '')
    fregesia = models.CharField(max_length=150, null=False, blank=False, default = '')
    telefone = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    profissao = models.CharField(max_length=150, null=True, blank=True)
    morada_emprego = models.CharField(max_length=150, null=True, blank=True)
    horario_trabalho = models.TimeField(null=True, blank=True)
    aluno_id = models.ForeignKey(to='aluno', on_delete=models.CASCADE, null=False, blank=False, default = '')

class Aluno_saida(models.Model):
    class Meta:
        db_table = 'aluno_saida'
    saida_id = models.AutoField(primary_key=True, null=False, blank=False, default = '')
    aluno_id = models.ForeignKey(to='aluno', on_delete=models.CASCADE, null=False, blank=False, default = '')
    hora_entrada = models.DateTimeField(null=True, blank=True)
    hora_saida = models.DateTimeField(null=True, blank=True)
    autorizacao_sair = models.CharField(max_length=250, null=True, blank=True)
    escolaridade = models.CharField(max_length=100, null=True, blank=True)

class Vacinacao(models.Model):
    class Meta:
        db_table = 'vacinacao'
    vac_id = models.AutoField(primary_key=True, null=False, blank=False, default = '')
    aluno_id = models.ForeignKey(to='aluno', on_delete=models.CASCADE, null=False, blank=False, default = '')
    vacina_name = models.CharField(max_length=250, null=False, blank=False, default = '')
    data_vacina = models.DateField(null=True, blank=True)
    plano_vacina = models.BooleanField(default= False, null=True, blank=True)

class Despesa(models.Model):
    class Meta:
        db_table = 'despesa'
    despesa_id = models.AutoField(primary_key=True, null=False, blank=False, default = '')
    categoria = models.CharField(max_length=250, null=False, blank=False, default = '')
    valor = models.FloatField(null=False, blank=False, default = '')
    descricao = models.CharField(max_length=250, null=False, blank=False, default = '')
    data = models.DateField(null=False, blank=False, default = '')

class Salario(models.Model):
    class Meta:
        db_table = 'salario'
    salario_id = models.AutoField(primary_key=True, null=False, blank=False, default = '')
    funcionario_id = models.ForeignKey(to='responsavel_educativo', on_delete=models.CASCADE, null=False, blank=False, default = '')
    valor = models.FloatField(null=False, blank=False, default = '')
    descricao = models.CharField(max_length=250, null=True, blank=True)
    data_pagamento = models.DateField(null=True, blank=True)
    subsidio_tipo = models.CharField(max_length=20, null=True, blank=True)
    subsidio_valor = models.FloatField(null=True, blank=True)

class Filiacao(models.Model):
    class Meta:
        db_table = 'filiacao'
    filiacao_id = models.AutoField(primary_key=True, null=False, blank=False, default = '')
    aluno_id = models.ForeignKey(to='aluno', on_delete=models.CASCADE, null=False, blank=False, default = '')
    respon_id = models.ForeignKey(to='responsavel_educativo', on_delete=models.CASCADE, null=False, blank=False, default = '')
    filiacao_responsavel = models.CharField(max_length=100, null=False, blank=False, default = '')

