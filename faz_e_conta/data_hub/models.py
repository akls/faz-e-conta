from django.db import models
import datetime
import django.utils as du

class Aluno(models.Model):
    class Meta:
        db_table = 'aluno'
    aluno_id = models.AutoField(primary_key=True)
    nome_proprio = models.CharField(max_length=100, default='')
    apelido = models.CharField(max_length=250, default='')
    processo = models.CharField(max_length=150, null=True, blank=True)
    data_admissao = models.DateField(default= du.timezone.now)
    data_ultima_renovacao = models.DateField(default= du.timezone.now, null=True, blank=True)
    data_nascimento = models.DateField(default= du.timezone.now)
    documento = models.CharField(max_length=250, default='')
    numero_documento = models.CharField(max_length=100, default='')
    data_validade = models.DateField(default= du.timezone.now)
    niss = models.IntegerField(null=True, blank=True)
    nif = models.IntegerField(null=True, blank=True)
    morada = models.CharField(max_length=150, default='')
    codigo_postal = models.CharField(max_length=150, default='')
    concelho = models.CharField(max_length=150, default='')
    fregesia = models.CharField(max_length=150, null=True, blank=True)
    escolaridade_anterior = models.CharField(max_length=150, null=True, blank=True)
    motivo_admissao = models.CharField(max_length=150, null=True, blank=True)
    cuidados_especias = models.CharField(max_length=150, null=True, blank=True)

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
    aluno_id = models.ForeignKey(to='Aluno', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome_proprio} {self. apelido}, Responsavel Educativo Id: {self.responsavel_educativo_id}"

class AlunoSaida(models.Model):
    class Meta:
        db_table = 'aluno_saida'
    aluno_saida_id = models.AutoField(primary_key=True)
    aluno_id = models.ForeignKey(to='Aluno', on_delete=models.CASCADE)
    hora_entrada = models.DateTimeField(null=True, blank=True)
    hora_saida = models.DateTimeField(null=True, blank=True)
    autorizacao_sair = models.CharField(max_length=250, null=True, blank=True)
    escolaridade = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.aluno_id} {self. hora_entrada}, Aluno Saida Id: {self.aluno_saida_id}"

class Vacinacao(models.Model):
    class Meta:
        db_table = 'vacinacao'
    vacinacao_id = models.AutoField(primary_key=True)
    aluno_id = models.ForeignKey(to='Aluno', on_delete=models.CASCADE)
    vacina_name = models.CharField(max_length=250, default='')
    data_vacina = models.DateField(default= du.timezone.now, null=True, blank=True)
    plano_vacina = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.aluno_id} {self. vacina_name}, Vacinacao Id: {self.vacinacao_id}"

class Despesa(models.Model):
    class Meta:
        db_table = 'despesa'
    despesa_id = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=250, default='')
    valor = models.FloatField()
    descricao = models.CharField(max_length=250, default='')
    data = models.DateField(default= du.timezone.now)

    def __str__(self):
        return f"{self.categoria} {self. valor}, Despesa Id: {self.despesa_id}"

class Salario(models.Model):
    class Meta:
        db_table = 'salario'
    salario_id = models.AutoField(primary_key=True)
    responsavel_educativo_id = models.ForeignKey(to='ResponsavelEducativo', on_delete=models.CASCADE)
    valor = models.FloatField()
    descricao = models.CharField(max_length=250, null=True, blank=True)
    data_pagamento = models.DateField(default= du.timezone.now, null=True, blank=True)
    subsidio_tipo = models.CharField(max_length=20, null=True, blank=True)
    subsidio_valor = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.responsavel_educativo_id} {self. valor}, Salario Id: {self.salario_id}"

class Filiacao(models.Model):
    class Meta:
        db_table = 'filiacao'
    filiacao_id = models.AutoField(primary_key=True)
    aluno_id = models.ForeignKey(to='Aluno', on_delete=models.CASCADE)
    responsavel_educativo_id = models.ForeignKey(to='ResponsavelEducativo', on_delete=models.CASCADE)
    filiacao_responsavel = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"{self.aluno_id} {self. responsavel_educativo_id}, Filiacao Id: {self.filiacao_id}"

