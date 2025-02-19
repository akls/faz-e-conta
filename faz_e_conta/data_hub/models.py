from django.db import models

class Aluno(models.Model):
    class Meta:
        db_table = 'aluno'
    aluno_id = models.AutoField(primary_key=True)
    nome_proprio = models.CharField(max_length=100)
    apelido = models.CharField(max_length=250)
    processo = models.CharField(max_length=150, null=True, blank=True)
    data_admissao = models.DateField()
    data_ultima_renovacao = models.DateField(null=True, blank=True)
    data_nascimento = models.DateField()
    documento = models.CharField(max_length=250)
    numero_documento = models.CharField(max_length=100)
    data_validade = models.DateField()
    niss = models.IntegerField(null=True, blank=True)
    nif = models.IntegerField(null=True, blank=True)
    morada = models.CharField(max_length=150)
    codigo_postal = models.CharField(max_length=150)
    concelho = models.CharField(max_length=150)
    fregesia = models.CharField(max_length=150, null=True, blank=True)
    escolaridade_anterior = models.CharField(max_length=150, null=True, blank=True)
    motivo_admissao = models.CharField(max_length=150, null=True, blank=True)
    cuidados_especias = models.CharField(max_length=150, null=True, blank=True)

class Responsavel_educativo(models.Model):
    class Meta:
        db_table = 'responsavel_educativo'
    respon_id = models.AutoField(primary_key=True)
    nome_proprio = models.CharField(max_length=100)
    apelido = models.CharField(max_length=250)
    data_nascimento = models.DateField()
    documento = models.CharField(max_length=150)
    numero_documento = models.IntegerField()
    data_validade = models.DateField()
    niss = models.IntegerField(null=True, blank=True)
    nif = models.IntegerField(null=True, blank=True)
    morada = models.CharField(max_length=250)
    codigo_postal = models.CharField(max_length=100)
    concelho = models.CharField(max_length=150)
    fregesia = models.CharField(max_length=150)
    telefone = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    profissao = models.CharField(max_length=150, null=True, blank=True)
    morada_emprego = models.CharField(max_length=150, null=True, blank=True)
    horario_trabalho = models.TimeField(null=True, blank=True)
    aluno_id = models.ForeignKey(to=aluno, on_delete=models.CASCADE)

class Aluno_saida(models.Model):
    class Meta:
        db_table = 'aluno_saida'
    saida_id = models.AutoField(primary_key=True)
    aluno_id = models.ForeignKey(to=aluno, on_delete=models.CASCADE)
    hora_entrada = models.DateTimeField(null=True, blank=True)
    hora_saida = models.DateTimeField(null=True, blank=True)
    autorizacao_sair = models.CharField(max_length=250, null=True, blank=True)
    escolaridade = models.CharField(max_length=100, null=True, blank=True)

class Vacinacao(models.Model):
    class Meta:
        db_table = 'vacinacao'
    vac_id = models.AutoField(primary_key=True)
    aluno_id = models.ForeignKey(to=aluno, on_delete=models.CASCADE)
    vacina_name = models.CharField(max_length=250)
    data_vacina = models.DateField(null=True, blank=True)
    plano_vacina = models.BooleanField(null=True, blank=True)

class Despesa(models.Model):
    class Meta:
        db_table = 'despesa'
    despesa_id = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=250)
    valor = models.FloatField()
    descricao = models.CharField(max_length=250)
    data = models.DateField()

class Salario(models.Model):
    class Meta:
        db_table = 'salario'
    salario_id = models.AutoField(primary_key=True)
    funcionario_id = models.ForeignKey(to=funcionario, on_delete=models.CASCADE)
    valor = models.FloatField()
    descricao = models.CharField(max_length=250, null=True, blank=True)
    data_pagamento = models.DateField(null=True, blank=True)
    subsidio_tipo = models.CharField(max_length=20, null=True, blank=True)
    subsidio_valor = models.FloatField(null=True, blank=True)

class Filiacao(models.Model):
    class Meta:
        db_table = 'filiacao'
    aluno_id = models.ForeignKey(primary_key=True, to=aluno, on_delete=models.CASCADE)
    respon_id = models.ForeignKey(to=responsavel_educativo, on_delete=models.CASCADE)
    filiacao_responsavel = models.CharField(max_length=100)

