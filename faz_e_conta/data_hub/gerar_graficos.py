import json
import os
import base64
import io

import matplotlib.pyplot as plt
from .models import *


def gerar_grafico_barras(x,y, title:str, rotation:int=0):
    # Criar gráfico de barras
    plt.figure(figsize=(12, 6),
               dpi=100, facecolor='white',
               edgecolor='black',
               linewidth=1.5,
               tight_layout=True,
               frameon=True)
    plt.bar(x[1], y[1], color='blue')
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


def Vacina_Quantidade():
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
                                  rotation=45)
    
    return grafico