from pyexpat.errors import messages
import textwrap
import matplotlib.pyplot as plt
from .gerar_graficos import *

import io
import csv
import os
import json
import base64


from django.shortcuts import redirect, render
from .forms import *
from .models import *
from .auto_gen_form_views import *
from .auto_gen_id_views import *
from django.db.models import Model
from django.apps import apps
from datetime import date, datetime, time
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.conf import settings

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

folder = "show_all/"



def index(request, counter: int = 5):
    graficos = []

    # Adiciona somente se o gráfico não for None
    for grafico in [
        ResponsavelEducativo_HorariosEntradaQuantidade(),
        Vacinacao_Quantidade(),
        Vacinacao_PlanoVacina()
    ]:
        if grafico is not None:
            graficos.append(grafico)

    return render(request, "index.html", {"counter": counter, "graficos": graficos})

def show_alunos(request):
    data = Aluno.objects.all()
    #head = [field.name for field in Aluno._meta.fields]
    
    head = ["aluno_id", "nome_proprio", "apelido", "processo", "numero_documento", "data_admissao"]
    
    # Melhorando a criação da lista de dicionários
    data_dict = list(data.values(*head))
    model = "Aluno"
    file_exists = json_exist(Aluno._meta.db_table.lower())
    
    return render(request, f"{folder}show_alunos.html", {"head": head, "data_dict": data_dict, "id": head[0], "model": model, 'file_exists': file_exists})


def show_responsaveis_educativos(request):
    data = ResponsavelEducativo.objects.all()    
    head = ["responsavel_educativo_id", "nome_proprio", "apelido", "numero_documento", "data_nascimento", "aluno_id"]
    
    # Melhorando a criação da lista de dicionários
    data_dict = list(data.values(*head))
    model = "ResponsavelEducativo"
    file_exists = json_exist(ResponsavelEducativo._meta.db_table.lower())
    
    return render(request, f"{folder}show_responsaveis_educativos.html", {"head": head, "data_dict": data_dict, "id": head[0], "model": model, 'file_exists': file_exists})


def show_vacinas(request):    
    data = Vacinacao.objects.all()
    head = [field.name for field in Vacinacao._meta.fields]

    # Melhorando a criação da lista de dicionários
    data_dict = list(data.values(*head))
    model = "Vacinacao"
    file_exists = json_exist(Vacinacao._meta.db_table.lower())
    
    return render(request, f"{folder}show_vacinas.html", {"head": head, "data_dict": data_dict, "id": head[0], "model": model, 'file_exists': file_exists})


def reports(request, model):
        folder = "report/"
        return render(request, f"{folder}gerar_vacinacao.html")

def reports_all(request):
        folder = "report/"
        return render(request, f"{folder}reports_page.html")



# Exports
def export_json(request, model):
    model_class = None
    for app in apps.get_app_configs():
        try:
            model_class = apps.get_model(app.label, model)
            break
        except LookupError:
            continue

    if not model_class:
        return HttpResponse(f'Modelo "{model}" não encontrado.', status=404)

    # Obter os dados da classe (modelo)
    model_data = model_class.objects.all()

    # Criar a estrutura de dados JSON
    data = []
    field_names = [field.name for field in model_class._meta.fields]
    
    def serialize_value(value):
        if isinstance(value, (date, datetime, time)):
            return str(value)  # Converter datas e horários para string
        if isinstance(value, Model):  # Verifica se é um objeto relacionado
            return value.pk  # Usa o ID do objeto relacionado
        return value
    
    for obj in model_data:
        item = {field: serialize_value(getattr(obj, field)) for field in field_names}
        data.append(item)

    # Definir o caminho para salvar o arquivo no diretório "resources/jsons"
    json_dir = os.path.join(settings.BASE_DIR, 'resources', 'jsons')
    os.makedirs(json_dir, exist_ok=True)
    file_path = os.path.join(json_dir, f'{model_class._meta.db_table.lower()}.json')

    # Salvar o JSON no arquivo
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    # Redirecionar de volta para a página anterior
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def export_csv(request, model):
    # Tente procurar o modelo no Django, usando o nome passado
    model_class = None
    for app in apps.get_app_configs():
        try:
            # Tente obter o modelo com o nome 'model_name' dentro do app
            model_class = apps.get_model(app.label, model)
            break  # Modelo encontrado, podemos parar a busca
        except LookupError:
            # Se o modelo não for encontrado neste app, continue buscando nos outros apps
            continue

    # Verifique se encontramos o modelo
    if not model_class:
        return HttpResponse(f'Modelo "{model}" não encontrado.', status=404)

    # Criar a resposta HTTP com o tipo de conteúdo correto para CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{model_class._meta.db_table.lower()}.csv"'

    # Criar o escritor CSV
    writer = csv.writer(response)

    # Definir os campos do cabeçalho do CSV (os nomes dos campos do modelo)
    field_names = [field.name for field in model_class._meta.fields]
    writer.writerow(field_names)

    # Obter os dados da classe (modelo)
    model_data = model_class.objects.all()

    # Iterar sobre os dados e escrever as linhas no CSV
    for obj in model_data:
        row = []
        for field in field_names:
            value = getattr(obj, field)
            # Verificar se o valor é um objeto relacionado (chave estrangeira ou similar)
            if isinstance(value, Model):  # Verifica se é uma instância de um modelo
                # Pode-se decidir aqui qual atributo do objeto relacionado exportar, por exemplo, o ID
                value = value.pk  # Ou qualquer outro atributo relacionado que queira exportar

            row.append(value)
        writer.writerow(row)

    return response

def download_json(request, model):
    for app in apps.get_app_configs():
        try:
            model_class = apps.get_model(app.label, model)
            break
        except LookupError:
            continue
    
    table = model_class._meta.db_table.lower()
    
    json_dir = os.path.join(settings.BASE_DIR, 'resources', 'jsons')
    os.makedirs(json_dir, exist_ok=True)
    json_file_path = os.path.join(json_dir, f'{table.lower()}.json')
    
    if os.path.exists(json_file_path):
        return FileResponse(open(json_file_path, 'rb'), as_attachment=True, filename=f"{table.lower()}.json")
    
    raise Http404("Ficheiro não encontrado")

def delete_json(request, model):
    # Define o caminho do arquivo JSON
    for app in apps.get_app_configs():
        try:
            model_class = apps.get_model(app.label, model)
            break
        except LookupError:
            continue
    
    table = model_class._meta.db_table.lower()
    
    json_dir = os.path.join(settings.BASE_DIR, 'resources', 'jsons')
    os.makedirs(json_dir, exist_ok=True)
    file_path = os.path.join(json_dir, f'{table.lower()}.json')
    
    
    # Verifica se o arquivo existe antes de tentar excluir
    if os.path.exists(file_path):
        try:
            os.remove(file_path)  # Deleta o arquivo
        except Exception as e:
            pass
    else:
        pass
    return redirect(request.META.get("HTTP_REFERER", "/"))  # Redireciona para a página anterior



# reports
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

    # Verifica o espaço disponível antes de adicionar a tabela
    available_height = doc.height - 100  # Ajuste conforme necessário
    table_height = table.wrap(doc.width, available_height)[1]

    

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
