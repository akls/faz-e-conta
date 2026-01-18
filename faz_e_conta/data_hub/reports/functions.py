from ..models import *

from django.db.models import Sum


def calcular_total_mensalidades():
    return MensalidadeAluno.objects.filter(mensalidade_paga__isnull=False).aggregate(
        total=Sum('mensalidade_paga')
    )['total'] or 0


def calcular_mensalidades_por_valencia():
    mensalidades_por_valencia = {}
    mensalidades = MensalidadeAluno.objects.select_related('aluno_id__sala_id').filter(mensalidade_paga__isnull=False)

    for m in mensalidades:
        valencia = m.aluno_id.sala_id.sala_valencia
        mensalidades_por_valencia[valencia] = mensalidades_por_valencia.get(valencia, 0) + m.mensalidade_paga

    return mensalidades_por_valencia


def calcular_total_mensalidades_ss():
    return ComparticipacaoMensalSs.objects.filter(mensalidade_paga__isnull=False).aggregate(
        total=Sum('mensalidade_paga')
    )['total'] or 0


def calcular_mensalidades_ss_por_valencia():
    mensalidades_por_valencia_ss = {}
    mensalidades = ComparticipacaoMensalSs.objects.select_related('aluno_id__sala_id').filter(mensalidade_paga__isnull=False)

    for m in mensalidades:
        valencia = m.aluno_id.sala_id.sala_valencia
        mensalidades_por_valencia_ss[valencia] = mensalidades_por_valencia_ss.get(valencia, 0) + m.mensalidade_paga

    return mensalidades_por_valencia_ss


def calcular_pagamentos_em_falta():
    dividas = Divida.objects.all()
    total_pagamentos_em_falta = 0

    for divida in dividas:
        try:
            valor_pagar = int(divida.valor_pagar)
        except (ValueError, TypeError):
            valor_pagar = 0

        try:
            valor_pago = int(divida.valor_pago) if divida.valor_pago is not None else 0
        except (ValueError, TypeError):
            valor_pago = 0

        total_pagamentos_em_falta += max(0, valor_pagar - valor_pago)

    return total_pagamentos_em_falta


def listar_pagamentos_em_falta():
    dividas = Divida.objects.select_related('aluno_id__sala_id')
    pagamentos_em_falta_list = []

    for divida in dividas:
        aluno = divida.aluno_id
        sala = aluno.sala_id
        valencia = sala.sala_valencia if sala else "Indefinido"

        # Conversão segura dos valores
        try:
            valor_pagar = int(divida.valor_pagar) if divida.valor_pagar is not None else 0
        except (ValueError, TypeError):
            valor_pagar = 0

        try:
            valor_pago = int(divida.valor_pago) if divida.valor_pago is not None else 0
        except (ValueError, TypeError):
            valor_pago = 0

        quantidade_falta = max(0, valor_pagar - valor_pago)

        ultimo_pagamento = MensalidadeAluno.objects.filter(aluno_id=aluno).order_by('-data_pagamento').first()

        pagamento_em_falta = {
            "Nome de aluno": f"{aluno.nome_proprio} {aluno.apelido}",
            "Valência": valencia,
            "Quantia mensal devida": valor_pagar,
            "Quantia em falta": quantidade_falta,
            "Data do último pagamento": getattr(ultimo_pagamento, 'data_pagamento', None),
            "Quantia do último pagamento": getattr(ultimo_pagamento, 'mensalidade_paga', None),
            "Valor pago pela SS": 0,  # Se necessário, implementar cálculo real
            "Data último pagamento SS": None,
            "Acordo": "Sim" if divida.acordo_set.exists() else "Não"
        }

        pagamentos_em_falta_list.append(pagamento_em_falta)

    return pagamentos_em_falta_list
