import textwrap

from ..gerar_graficos import *
from .functions import *


import io
import base64

from ..models import *

from django.apps import apps
from django.http import FileResponse, HttpResponse
from datetime import datetime

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from PyPDF2 import PdfMerger
from django.contrib.auth.decorators import login_required


login_url = 'login'
@login_required(login_url=login_url)
def gerar_pdf(request, model):
    model_class = None

    # Verifica se o modelo existe em qualquer app
    for app in apps.get_app_configs():
        try:
            model_class = apps.get_model(app.label, model)
            break
        except LookupError:
            continue

    # Se o modelo não foi encontrado, retorna erro
    if not model_class:
        return HttpResponse("Modelo não encontrado", status=404)

    # Obtém os dados do modelo
    objetos = model_class.objects.all()

    # Cria um buffer de memória para o PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    elements = []

    # Adiciona cabeçalho ao PDF
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Relatório: {model}", styles['Title']))
    elements.append(Paragraph(f"Total de registros: {objetos.count()}", styles['Normal']))
    elements.append(Spacer(1, 6))

    # Adiciona dados ao PDF em formato de tabela
    data = []  # Cabeçalhos da tabela
    for obj in objetos:
        wrapped_text = textwrap.wrap(str(obj), width=70)  # Ajusta a largura conforme necessário
        data.append(["\n".join(wrapped_text)])

    table = Table(data)
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))


    elements.append(table)

    # Obtém gráficos gerados dinamicamente (base64)
    graficos = graficos_modelo(model)  
    
    # Adiciona gráficos ao PDF
    for grafico_base64 in graficos:
        if grafico_base64:  # Se o gráfico não for None
            grafico_bytes = base64.b64decode(grafico_base64)  # Converte base64 para bytes
            img = ImageReader(io.BytesIO(grafico_bytes))  # Cria um objeto ImageReader
            elements.append(img)
            elements.append(Spacer(1, 220))  # Espaço após o gráfico

    # Finaliza e salva o PDF
    if elements:
        doc.build(elements)

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{model}_relatorio.pdf")

@login_required(login_url=login_url)
def gerar_pdf_aluno(request, aluno_id):
    # Obtém os dados do modelo
    aluno = Aluno.objects.get(aluno_id=aluno_id)
    
    # Verifica se o aluno existe
    if not aluno:
        return HttpResponse("Aluno não encontrado", status=404)
    
    
    # Cria um buffer de memória para o PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    elements = []

    # Adiciona cabeçalho ao PDF
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Relatório do {aluno}", styles['Title']))
    elements.append(Spacer(1, 6))

    
    head = [field.name for field in Aluno._meta.fields]


    # Adiciona dados ao PDF em formato de tabela
    data = []  # Cabeçalhos da tabela
    for field in head:
        wrapped_text = textwrap.wrap(str(getattr(aluno, field)), width=70)  # Ajusta a largura conforme necessário
        data.append([field, "\n".join(wrapped_text)])

    table = Table(data)
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    # Finaliza e salva o PDF
    if elements:
        doc.build(elements)

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{str(aluno)}_relatorio.pdf")

@login_required(login_url=login_url)
def reportAlunoSala(request):
    # Obtém o modelo de Aluno e Sala
    for app in apps.get_app_configs():
        try:
            Aluno = apps.get_model(app.label, 'Aluno')
            Sala = apps.get_model(app.label, 'Sala')
            break
        except LookupError:
            continue

    # Verifica se os modelos existem
    if not (Aluno and Sala):
        return HttpResponse("Modelos não encontrados", status=404)

    # Cria um buffer de memória para o PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    elements = []
    styles = getSampleStyleSheet()

    # Adiciona cabeçalho ao PDF
    elements.append(Paragraph("Relatório de Alunos por Sala", styles['Title']))
    elements.append(Spacer(1, 12))

    # Obtém todas as salas
    salas = Sala.objects.all()

    for sala in salas:
        # Adiciona título da sala
        elements.append(Paragraph(f"Sala: {sala.sala_nome}", styles['Heading2']))
        elements.append(Spacer(1, 12))

        # Obtém alunos da sala
        alunos = Aluno.objects.filter(sala_id=sala.sala_id)

        # Cria tabela de alunos
        data = [["ID", "Nome", "Apelido", "Processo", "Numero\nDocumento", "Data\nAdmissao"]]
        
        #for i in range(20):
        for aluno in alunos:
            data.append([
                aluno.aluno_id,
                Paragraph(aluno.nome_proprio, styles['Normal']),
                Paragraph(aluno.apelido, styles['Normal']),
                Paragraph(aluno.processo, styles['Normal']),
                Paragraph(aluno.numero_documento, styles['Normal']),
                Paragraph(str(aluno.data_admissao).split(" ")[0], styles['Normal'])
            ])

        table = Table(data, colWidths=[doc.width / 6.0] * 6)  # Ajusta a largura das colunas
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinha verticalmente ao meio
            ('FONTSIZE', (0, 0), (-1, -1), 10),  # Define o tamanho da fonte
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Cor do texto para as linhas de dados
        ]))

        elements.append(table)
        elements.append(PageBreak())

    # Finaliza e salva o PDF
    doc.build(elements)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="relatorio_alunos_sala.pdf")

# Other reports
@login_required(login_url=login_url)
def reportMensal(request, month=None, year=None):
    bullet_icons = ['➼', '➾', '➔']
    now = datetime.now()
    date_time = now.strftime('%d-%m-%Y %H:%M:%S')
    styles = getSampleStyleSheet()
    wrap_style = ParagraphStyle('WrapStyle', parent=styles['Normal'], wordWrap='CJK')

    # ---------- Parte 1: Relatório vertical ----------
    buffer1 = io.BytesIO()
    doc1 = SimpleDocTemplate(buffer1, pagesize=A4)
    elements1 = []
    if month == None or year == None:
        elements1.append(Paragraph(f"Relatório gerado a {date_time}", styles['Title']))
        elements1.append(Spacer(1, 12))
    else:
        elements1.append(Paragraph(f"Relatório do mes {month}/{year}", styles['Title']))
        elements1.append(Paragraph(f"Gerado a {date_time}", styles['Title']))

    elements1.append(Spacer(1, 12))
    elements1.append(Spacer(1, 12))

    graph_path = gerar_grafico_numero_alunos_por_valencia()
    elements1.append(Image(graph_path, width=400, height=200))
    elements1.append(Spacer(1, 12))

    total_fees_paid_by_students = float(calcular_total_mensalidades() or 0)
    elements1.append(PageBreak())
    elements1.append(Paragraph(f"Valor total de mensalidades pagas pelos alunos: {total_fees_paid_by_students:.2f}€", styles['Title']))
    elements1.append(Spacer(1, 12))

    graph_path = gerar_grafico_mensalidades_por_valencia()
    elements1.append(Image(graph_path, width=400, height=200))
    elements1.append(Spacer(1, 12))

    for valence, amount in calcular_mensalidades_por_valencia().items():
        elements1.append(Paragraph(f"{bullet_icons[0]} Valor por valência ({valence}): {amount:.2f}€", styles['Normal']))
        elements1.append(Spacer(1, 12))

    total_fees_paid_by_ss = float(calcular_total_mensalidades_ss() or 0)
    elements1.append(PageBreak())
    elements1.append(Paragraph(f"Valor total de mensalidades pagas pela SS: {total_fees_paid_by_ss:.2f}€", styles['Title']))
    elements1.append(Spacer(1, 12))

    graph_path = gerar_grafico_mensalidades_SS_por_valencia()
    elements1.append(Image(graph_path, width=400, height=200))
    elements1.append(Spacer(1, 12))

    for valence, amount in calcular_mensalidades_ss_por_valencia().items():
        elements1.append(Paragraph(f"{bullet_icons[0]} Valor pela SS por valência ({valence}): {amount:.2f}€", styles['Normal']))
        elements1.append(Spacer(1, 12))


    doc1.build(elements1)

    # ---------- Parte 2: Tabela horizontal ----------
    buffer2 = io.BytesIO()
    doc2 = SimpleDocTemplate(buffer2, pagesize=landscape(A4), leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    elements2 = []

    payments_in_default = float(calcular_pagamentos_em_falta() or 0)
    elements2.append(Paragraph(f"Valor de pagamentos de alunos em falta: {payments_in_default:.2f}€", styles['Title']))
    elements2.append(Spacer(1, 12))

    pagamentos = listar_pagamentos_em_falta()
    table_data = [[
        Paragraph("Nome de aluno", wrap_style),
        Paragraph("Valência", wrap_style),
        Paragraph("Quantia mensal devida", wrap_style),
        Paragraph("Quantia em falta", wrap_style),
        Paragraph("Data do último pagamento", wrap_style),
        Paragraph("Quantia do último pagamento", wrap_style),
        Paragraph("Valor pago pela SS", wrap_style),
        Paragraph("Data último pagamento SS", wrap_style),
        Paragraph("Acordo", wrap_style),
    ]]

    for p in pagamentos:
        table_data.append([
            Paragraph(str(p["Nome de aluno"]), wrap_style),
            Paragraph(str(p["Valência"]), wrap_style),
            Paragraph(str(p["Quantia mensal devida"]), wrap_style),
            Paragraph(str(p["Quantia em falta"]), wrap_style),
            Paragraph(str(p["Data do último pagamento"]), wrap_style),
            Paragraph(str(p["Quantia do último pagamento"]), wrap_style),
            Paragraph(str(p["Valor pago pela SS"]), wrap_style),
            Paragraph(str(p["Data último pagamento SS"]), wrap_style),
            Paragraph(str(p["Acordo"]), wrap_style),
        ])

    col_widths = [100, 80, 70, 70, 85, 75, 75, 85, 70]
    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    elements2.append(KeepTogether(table))
    doc2.build(elements2)

    # ---------- Parte 3: Info Final ----------
    buffer3 = io.BytesIO()
    doc3 = SimpleDocTemplate(buffer3, pagesize=A4)
    elements3 = []
    
    if month == None or year == None:
        DespesasFixas = DespesaFixa.objects.all().values('valor')
        DespesasVariaveis = DespesasVariavel.objects.all().values('valor')
    else: 
        DespesasFixas = DespesaFixa.objects.filter(data__month=month, data__year=year).values('valor')
        DespesasVariaveis = DespesasVariavel.objects.filter(data__month=month, data__year=year).values('valor')
    
    fixed_expenses = float(DespesasFixas.aggregate(sum=Sum('valor'))['sum'] or 0)
    variable_expenses = float(DespesasVariaveis.aggregate(sum=Sum('valor'))['sum'] or 0)
    
    total_students = Aluno.objects.count() or 1
    
    cost_per_student = (
        fixed_expenses + variable_expenses - (total_fees_paid_by_students + total_fees_paid_by_ss)
    ) / total_students *-1
    
    final_balance = (
        total_fees_paid_by_students + total_fees_paid_by_ss
        - fixed_expenses - variable_expenses - payments_in_default
    )
    
    
    if month == None or year == None:
        elements3.append(Paragraph(f"Despesas Gerais:", styles['Title']))
        elements3.append(Paragraph(f"Despesas fixas Gerais: {fixed_expenses:.2f}€", styles['Normal']))
        elements3.append(Spacer(1, 12))
        elements3.append(Paragraph(f"Despesas variáveis Gerais: {variable_expenses:.2f}€", styles['Normal']))
        elements3.append(Spacer(1, 12))
    else:
        elements3.append(Paragraph(f"Despesas do mes:", styles['Title']))
        elements3.append(Paragraph(f"Despesas fixas do mês: {fixed_expenses:.2f}€", styles['Normal']))
        elements3.append(Spacer(1, 12))
        elements3.append(Paragraph(f"Despesas variáveis do mês: {variable_expenses:.2f}€", styles['Normal']))
        elements3.append(Spacer(1, 12))
    
    
    if cost_per_student > 0:
        elements3.append(Paragraph(f"Valor médio por aluno: {cost_per_student:.2f}€", styles['Normal']))
    else:
        elements3.append(Paragraph(f"Valor médio por aluno: <font color='red'>{cost_per_student:.2f}€</font>", styles['Normal']))
    elements3.append(Spacer(1, 12))
    
    
    if final_balance > 0:
        elements3.append(Paragraph(f"Balanço final: {final_balance:.2f}€", styles['Normal']))
    else:
        elements3.append(Paragraph(f"Balanço final: <font color='red'>{final_balance:.2f}€</font>", styles['Normal']))
    elements3.append(Spacer(1, 12))

    doc3.build(elements3)

    # ---------- Merge de tudo ----------
    final_buffer = io.BytesIO()
    merger = PdfMerger()
    buffer1.seek(0)
    buffer2.seek(0)
    buffer3.seek(0)
    merger.append(buffer1)
    merger.append(buffer2)
    merger.append(buffer3)
    merger.write(final_buffer)
    merger.close()
    final_buffer.seek(0)

    return FileResponse(final_buffer, as_attachment=True, filename=f"relatorio_mensal_{str(date_time).split(" ")[0]}_{str(date_time).split(" ")[1].replace(":", "-")}.pdf")
