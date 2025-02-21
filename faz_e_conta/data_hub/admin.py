from django.contrib import admin
from .models import Aluno, Responsavel_educativo, Aluno_saida, Vacinacao, Despesa, Salario, Filiacao

# Register your models here.
admin.site.register(Aluno)
admin.site.register(Responsavel_educativo)
admin.site.register(Aluno_saida)
admin.site.register(Vacinacao)
admin.site.register(Despesa)
admin.site.register(Salario)
admin.site.register(Filiacao)