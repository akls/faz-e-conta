from django.db import models


class Aluno(models.Model):
    class Meta:
        db_table = "aluno"

    aluno_id = models.BigAutoField(primary_key=True)
    nome_proprio = models.CharField(max_length=100)
    apelido = models.CharField(max_length=250)
    processo = models.CharField(max_length=100, null=True, blank=True)
    