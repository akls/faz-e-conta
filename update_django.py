import pandas as pd
import datetime





# Função para criar os modelos
def create_model(df, table_name):
    info = f"""class {table_name.capitalize()}(models.Model):
    class Meta:
        db_table = '{table_name}'
"""

    for _, row in df.iterrows():
        field_declaration = f"    {row['column_name']} = models.{row['django_field_type']}("
        params = []
        
        # ID automático
        if row["auto_id"] == "Yes":
            params.append("primary_key=True")
        
        # Se for CharField, verificar max_length
        if row["django_field_type"] == "CharField":
            max_length = int(row["datatype_parameters"]) if pd.notna(row["datatype_parameters"]) else 255
            params.append(f"max_length={max_length}")

        # Se for ForeignKey, definir corretamente
        if row["django_field_type"] == "ForeignKey":
            params.append(f"to='{row['datatype_parameters']}', on_delete=models.CASCADE")

        # Se for BooleanField, definir default corretamente
        if row["django_field_type"] == "BooleanField":
            default_value = False if pd.isna(row["datatype_parameters"]) else row["datatype_parameters"]
            params.append(f"default={default_value}")

        # Se for DateField, corrigir default inválido
        if row["django_field_type"] == "DateField":
            params.append("default= du.timezone.now")

        # Restrições de NULL
        if row["null_constraint"] != "NOT NULL":
            params.append("null=True, blank=True")
        else:
            if row["django_field_type"] == "CharField":
                params.append("default=''")
            elif row["django_field_type"] == "BooleanField":
                params.append("default=False")

        # Montar a linha final do campo
        field_declaration += ", ".join(params) + ")"
        info += field_declaration + "\n"
        
    return info

# Função para ler o CDM e criar os modelos automaticamente
def read_cdm(file_path: str, models_path: str, admin_path: str, forms_path: str, sheet_name="Table Summary"):
    try:
        table_summary_df = pd.read_excel(file_path, sheet_name)
        class_list = []
        
        if "table_name" not in table_summary_df.columns:
            print("Erro: A coluna 'table_name' não está presente na planilha 'Table Summary'.")
            return

        with open(models_path, "w", encoding="utf-8") as arquivo:
            arquivo.write("from django.db import models\nimport datetime\nimport django.utils as du\n\n")

            table_names = table_summary_df["table_name"].dropna().tolist()
            for table_name in table_names:
                try:
                    sheet_df = pd.read_excel(file_path, sheet_name=table_name)
                    if not sheet_df.empty:
                        model_code = create_model(sheet_df, table_name)
                        arquivo.write(f"{model_code}\n")
                        class_list.append(table_name.capitalize())
                except Exception as e:
                    print(f"Erro ao ler a planilha '{table_name}': {e}")
        
        # Adicionar as classes ao arquivo admin.py
        with open(admin_path, "w", encoding="utf-8") as arquivo:
            arquivo.write("from django.contrib import admin\n")
            arquivo.write(f"from .models import {', '.join(class_list)}\n\n")
            arquivo.write("# Register your models here.\n\n")
            for table_name in class_list:
                arquivo.write(f"admin.site.register({table_name})\n")
                
        # Adicionar as classes ao arquivo forms.py
        with open(forms_path, "w", encoding="utf-8") as arquivo:
            arquivo.write("from django import forms\n")
            arquivo.write(f"from .models import {', '.join(class_list)}\n")
            arquivo.write("from .widgets import *\n")
            arquivo.write("\n")
            for table_name in class_list:
                sheet_df = pd.read_excel(file_path, sheet_name=table_name.lower())
                arquivo.write(f"class {table_name}Form(forms.ModelForm):\n")
                arquivo.write("    class Meta:\n")
                arquivo.write(f"        model = {table_name}\n")
                arquivo.write("        fields = ['" + "', '".join(sheet_df["column_name"].tolist()) + "']\n\n")
                arquivo.write("        # Adiciona atributos aos campos do formulário\n")
                arquivo.write(f"        widgets = {table_name}_widget()\n\n")
    except Exception as e:
        print(f"Erro ao ler a planilha 'Table Summary': {e}")

# Caminhos dos arquivos
file_path = "resources/cdm/cdm_fazeconta.xlsx"
models_path = "faz_e_conta/data_hub/models.py"
admin_path = "faz_e_conta/data_hub/admin.py"
forms_path = "faz_e_conta/data_hub/forms.py"

# Executar o gerador
read_cdm(file_path, models_path, admin_path, forms_path)
