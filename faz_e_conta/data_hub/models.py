from django.db import models

class Aluno(models.Model):
    class Meta:
        db_table = 'aluno'
    aluno_id = models.INTEGER(primary_key=True)
    nome_proprio = models.TEXT()
    apelido = models.TEXT()
    processo = models.TEXT()
    data_admissao = models.TEXT()
    data_renovacao = models.TEXT()
    data_nascimento = models.TEXT()
    documento = models.TEXT()
    numero_documento = models.TEXT()
    data_validade = models.TEXT()
    niss = models.INTEGER()
    nif = models.INTEGER()
    morada = models.TEXT()
    codigo_postal = models.TEXT()
    concelho = models.TEXT()
    fregesia = models.TEXT()
    escolaridade_anterior = models.TEXT()
    motivo_admissao = models.TEXT()
    cuidados_especias = models.TEXT()

class Responsavel_educativo(models.Model):
    class Meta:
        db_table = 'responsavel_educativo'
    respon_id = models.INTEGER(primary_key=True)
    nome_proprio = models.TEXT()
    apelido = models.TEXT()
    data_admissao = models.TEXT()
    data_renovacao = models.TEXT()
    data_nascimento = models.TEXT()
    documento = models.TEXT()
    numero_documento = models.TEXT()
    data_validade = models.TEXT()
    niss = models.INTEGER()
    nif = models.INTEGER()
    morada = models.TEXT()
    codigo_postal = models.TEXT()
    concelho = models.TEXT()
    fregesia = models.TEXT()
    contacto = models.INTEGER()
    email = models.TEXT()
    profissao = models.TEXT()
    morada_emprego = models.TEXT()
    horario_trabalho = models.TEXT()
    aluno_id = models.INTEGER()

class Aluno_saida(models.Model):
    class Meta:
        db_table = 'aluno_saida'
    saida_id = models.INTEGER(primary_key=True)
    aluno_id = models.INTEGER()
    hora_entrada = models.NUMERIC()
    hora_saida = models.NUMERIC()
    autorizacao_sair = models.TEXT()
    escolaridade = models.TEXT()

class Vacinacao(models.Model):
    class Meta:
        db_table = 'vacinacao'
    vac_id = models.INTEGER(primary_key=True)
    aluno_id = models.INTEGER()
    vacina_name = models.TEXT()
    data_vacina = models.NUMERIC()
    plano_vacina = models.BLOB()

