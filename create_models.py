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
            params.append("default= django.utils.timezone.now")

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
def read_cdm(file_path: str, models_path: str, sheet_name="Table Summary"):
    try:
        table_summary_df = pd.read_excel(file_path, sheet_name)
        if "table_name" not in table_summary_df.columns:
            print("Erro: A coluna 'table_name' não está presente na planilha 'Table Summary'.")
            return

        with open(models_path, "w", encoding="utf-8") as arquivo:
            arquivo.write("from django.db import models\nimport datetime\n\n")

            table_names = table_summary_df["table_name"].dropna().tolist()
            for table_name in table_names:
                try:
                    sheet_df = pd.read_excel(file_path, sheet_name=table_name)
                    if not sheet_df.empty:
                        model_code = create_model(sheet_df, table_name)
                        arquivo.write(f"{model_code}\n")
                except Exception as e:
                    print(f"Erro ao ler a planilha '{table_name}': {e}")
    except Exception as e:
        print(f"Erro ao ler a planilha 'Table Summary': {e}")

# Caminhos dos arquivos
file_path = "resources/cdm/cdm_fazeconta.xlsx"
models_path = "faz_e_conta/data_hub/models.py"

# Executar o gerador
read_cdm(file_path, models_path)
