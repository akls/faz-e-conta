import json
import os
import base64
import io
import random

from django.conf import settings
import matplotlib.pyplot as plt
from .models import *
from .models import Imagem  # Certifique-se de que o modelo Grafico está definido


palette = [
    (0.90, 0.10, 0.10),  # Vermelho intenso
    (0.10, 0.60, 0.10),  # Verde médio
    (0.10, 0.10, 0.90),  # Azul forte
    (0.95, 0.75, 0.10),  # Amarelo dourado
    (0.80, 0.10, 0.80),  # Magenta vibrante
    (0.10, 0.80, 0.80),  # Ciano suave
    (0.60, 0.60, 0.60),  # Cinza neutro
    (1.00, 0.50, 0.00),  # Laranja quente
    (0.50, 0.10, 0.90),  # Roxo profundo
    (0.40, 0.80, 0.40),  # Verde claro
    (1.00, 0.50, 0.70),  # Rosa vibrante
    (0.40, 0.40, 1.00),  # Azul brilhante
    (0.80, 0.40, 0.00),  # Marrom alaranjado
    (0.60, 0.20, 0.00),  # Bordô escuro
    (0.00, 0.60, 0.40),  # Verde esmeralda
    (0.70, 0.00, 0.70),  # Púrpura
    (0.50, 0.50, 0.00),  # Oliva
    (0.10, 0.40, 0.80),  # Azul céu
    (0.80, 0.80, 0.10),  # Mostarda
    (0.20, 0.20, 0.20)   # Preto suave
]

path = os.path.join(settings.BASE_DIR, 'static', 'graficos/')
os.makedirs(path, exist_ok=True) 

def json_exist(model):
    json_dir = os.path.join(settings.BASE_DIR, 'resources', 'jsons')
    os.makedirs(json_dir, exist_ok=True)
    file_path = os.path.join(json_dir, f'{model}.json')
    print(file_path)
    return os.path.exists(file_path)
    
def gerar_grafico_barras(x,y, title:str, rotation:int=0, multi_color:bool=False):
    # Criar gráfico de barras
    plt.figure(figsize=(12, 6),
               dpi=100, facecolor='white',
               edgecolor='black',
               linewidth=1.5,
               tight_layout=True,
               frameon=True)
    
    # Ao criar o gráfico
    colors = []
    if multi_color:
        for i in range(len(y[1])):
            color = palette[i % len(palette)]  # Chama a função passando a última cor
            colors.append(color)
    else:
        colors = ["blue"] * len(y[1])
    
    plt.bar(x[1], y[1], color= colors)
    plt.xlabel(f"{x[0]}")
    plt.ylabel(f"{y[0]}")
    plt.title(f"{title}")
    
    plt.xticks(rotation=rotation, ha='right')
    
    # Salvar gráfico na memória
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    grafico = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    
    return grafico

def gerar_grafico_pizza(x,y, title:str, rotation:int=0):
    # Criar gráfico de pizza
    plt.figure(figsize=(12, 6),
               dpi=100, facecolor='white',
               edgecolor='black',
               linewidth=1.5,
               tight_layout=True,
               frameon=True)
    
    # Ao criar o gráfico
    plt.pie(y[1], labels=x[1], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.title(f"{title}")
    
    # Salvar gráfico na memória
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    grafico = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    
    return grafico



# Graficos Relatorios
def gerar_grafico_barras_relatorios(x,y, title:str, rotation:int=0, multi_color:bool=False, palette:tuple=palette):
        # Criar gráfico de barras
    plt.figure(figsize=(12, 6),
               dpi=100, facecolor='white',
               edgecolor='black',
               linewidth=1.5,
               tight_layout=True,
               frameon=True)
    
    # Ao criar o gráfico
    colors = []
    if multi_color:
        for i in range(len(y[1])):
            color = palette[i % len(palette)]  # Chama a função passando a última cor
            colors.append(color)
    else:
        colors = ["blue"] * len(y[1])
    
    plt.bar(x[1], y[1], color= colors)
    plt.xlabel(f"{x[0]}")
    plt.ylabel(f"{y[0]}")
    plt.title(f"{title}")
    
    plt.xticks(rotation=rotation, ha='right')
    
    # Salvar gráfico na memória
    graph_path = f"{path}{title}.png"
    plt.savefig(graph_path)
    
    return graph_path

def gerar_grafico_pizza_relatorios(x,y, title:str, rotation:int=0, multi_color:bool=False):
    # Criar gráfico de pizza
    plt.figure(figsize=(12, 6),
               dpi=100, facecolor='white',
               edgecolor='black',
               linewidth=1.5,
               tight_layout=True,
               frameon=True
               )
    
    # Ao criar o gráfico
    plt.pie(y[1], labels=x[1], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.title(f"{title}")
    
    # Salvar gráfico na memória
    graph_path = f"{path}{title}.png"
    
    plt.savefig(graph_path)
    
    return graph_path

# Graficos bd
def gerar_grafico_barras_bd(x,y, title:str, rotation:int=0, multi_color:bool=False):
    # Criar gráfico de barras
    plt.figure(figsize=(12, 6),
               dpi=100, facecolor='white',
               edgecolor='black',
               linewidth=1.5,
               tight_layout=True,
               frameon=True)
    # Ao criar o gráfico
    colors = []
    if multi_color:
        for i in range(len(y[1])):
            color = palette[i % len(palette)]
            colors.append(color)
    else:
        colors = ["blue"] * len(y[1])
    plt.bar(x[1], y[1], color= colors)
    plt.xlabel(f"{x[0]}")
    plt.ylabel(f"{y[0]}")
    plt.title(f"{title}")
    plt.xticks(rotation=rotation, ha='right')
    # Salvar gráfico na memória
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    grafico = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    # Inserir ou atualizar gráfico na base de dados
    grafico_obj, created = Grafico.objects.update_or_create(
        titulo=title,
        defaults={
            'imagem': grafico,
            'tipo': 'barras',  # Tipo do gráfico
            'dados_x': json.dumps(x[1]),
            'dados_y': json.dumps(y[1])
        }
    )
    return grafico

# Todos Classe
def graficos_modelo(model:str):
    if model.lower() == "vacinacao".lower():
        return Vacinacao_graficos()
    else:
        return []

def Vacinacao_graficos():
    graficos = []
    for grafico in [
        Vacinacao_Quantidade(),
        Vacinacao_PlanoVacina()
    ]:
        if grafico is not None:
            graficos.append(grafico)
    return graficos


# Modelo_MomeGrafico
def ResponsavelEducativo_HorariosEntradaQuantidade():
    json_name = "responsavel_educativo.json"
    try:
        responsaveis = json.load(open(f"./resources/jsons/{json_name}", "r", encoding="utf-8"))
    except FileNotFoundError:
        return None

    
    # Filtrar responsáveis com horário de trabalho não nulo
    dict_time = {}
    for responsavel in responsaveis:
        if responsavel['horario_trabalho'].split(":")[0] not in dict_time:
            dict_time[responsavel['horario_trabalho'].split(":")[0]] = 1
        else:
            dict_time[responsavel['horario_trabalho'].split(":")[0]] = dict_time[responsavel['horario_trabalho'].split(":")[0]]+1
        
    dict_time = dict(sorted(dict_time.items(), key=lambda item: item[0]))
        
    grafico = gerar_grafico_barras(["Hora de entrada",[f"{horario}:00 - {int(horario)+1 if horario != 23 else 0}:00" for horario in dict_time.keys()]],
                                  ["Numero de Responsaveis", dict_time.values()], 
                                  "Numero de Responsaveis a entrar por hora")
    
    return grafico

def Vacinacao_Quantidade():
    json_name = "vacinacao.json"
    try:
        vacinas = json.load(open(f"./resources/jsons/{json_name}", "r", encoding="utf-8"))
    except FileNotFoundError:
        return None
    
    dict_vacinas = {}
    for vacina in vacinas:
        if vacina['vacina_name'] not in dict_vacinas:
            dict_vacinas[vacina['vacina_name']] = 1
        else:
            dict_vacinas[vacina['vacina_name']] = dict_vacinas[vacina['vacina_name']]+1
    
    dict_vacinas = dict(sorted(dict_vacinas.items(), key=lambda item: item[0]))
    grafico = gerar_grafico_barras(["Vacina", dict_vacinas.keys()],
                                  ["Numero de Vacinas", dict_vacinas.values()], 
                                  "Numero de Vacinas por Tipo",
                                  rotation=45,
                                  multi_color=True)
    
    return grafico

def Vacinacao_PlanoVacina():
    json_name = "vacinacao.json"
    try:
        vacinas = json.load(open(f"./resources/jsons/{json_name}", "r", encoding="utf-8"))
    except FileNotFoundError:
        return None
    
    dict_vacinas = {"Sim": 0,
                    "Não": 0}
    for vacina in vacinas:
        if vacina["plano_vacina"]:
            dict_vacinas["Sim"] += 1
        else:
            dict_vacinas["Não"] += 1
    
    grafico = gerar_grafico_barras(["Plano Vacina", dict_vacinas.keys()],
                                  ["Numero", dict_vacinas.values()], 
                                  "Numero de Vacinas por Tipo")
    
    return grafico



# Other
def gerar_grafico_numero_alunos_por_valencia():
    valencias = Sala.objects.values_list('sala_valencia', flat=True).distinct()
    alunos = Aluno.objects.all()
    
    num_alunos = {valencia: 0 for valencia in valencias}
    
    for aluno in alunos:
        valencia = aluno.sala_id.sala_valencia
        num_alunos[valencia] += 1
    
    grafico = gerar_grafico_barras_relatorios(["Valência", num_alunos.keys()],
                                  ["Número de Alunos", num_alunos.values()], 
                                  "Número de Alunos por Valência",
                                  rotation=0,
                                  multi_color=True)
    
    return grafico


def gerar_grafico_mensalidades_por_valencia():
    valencias = Sala.objects.values_list('sala_valencia', flat=True).distinct()
    mensalidades = MensalidadeAluno.objects.all()
    
    num_mensalidades = {valencia: 0 for valencia in valencias}
    
    for mensalidade in mensalidades:
        aluno = Aluno.objects.get(aluno_id = mensalidade.aluno_id.aluno_id)
        valencia = aluno.sala_id.sala_valencia
        num_mensalidades[valencia] += 1
    
    grafico = gerar_grafico_pizza_relatorios(["Valência", num_mensalidades.keys()],
                                  ["Número de Mensalidades", num_mensalidades.values()], 
                                  "Número de Mensalidades por Valência",
                                  rotation=0,
                                  multi_color=True)
    
    return grafico


def gerar_grafico_mensalidades_SS_por_valencia():
    valencias = Sala.objects.values_list('sala_valencia', flat=True).distinct()
    mensalidades = ComparticipacaoMensalSs.objects.all()
    
    num_mensalidades = {valencia: 0 for valencia in valencias}
    
    for mensalidade in mensalidades:
        aluno = Aluno.objects.get(aluno_id = mensalidade.aluno_id.aluno_id)
        valencia = aluno.sala_id.sala_valencia
        num_mensalidades[valencia] += 1
    
    grafico = gerar_grafico_pizza_relatorios(["Valência", num_mensalidades.keys()],
                                  ["Número de Mensalidades SS", num_mensalidades.values()], 
                                  "Número de Mensalidades SS por Valência",
                                  rotation=0,
                                  multi_color=True)
    
    return grafico


def gerar_grafico_alunos_por_sala():
    salas = Sala.objects.values_list('sala_nome', flat=True).distinct()
    alunos = Aluno.objects.all()
    
    num_alunos = {sala: 0 for sala in salas}
    
    for aluno in alunos:
        sala = aluno.sala_id.sala_nome
        num_alunos[sala] += 1
    
    new_palette = palette        
       
    grafico = gerar_grafico_barras_relatorios(["Sala", num_alunos.keys()],
                                    ["Número de Alunos", num_alunos.values()], 
                                    "Número de Alunos por Sala",
                                    rotation=45,
                                    multi_color=True,
                                    palette=new_palette)
    
    return grafico