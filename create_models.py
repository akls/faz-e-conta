import pandas as pd

# CREATE THE MODELS.PY FILE OR UPDATE IT

def create_model (df, table_name):
    info = f"""class {table_name.capitalize()}(models.Model):
    class Meta:
        db_table = '{table_name}'
"""

    for _, row in df.iterrows():
        remove_last = False
        info += f"    {row["column_name"]} = models.{row["django_field_type"]}("
        
        # Id
        if row["auto_id"] == "Yes":
            info += "primary_key=True, "
            remove_last = True
        
        # Se tiver tamanho definido
        if row["django_field_type"] == "CharField":
            if pd.isna(row["datatype_parameters"]) != True:
                info+= f"max_length={int(row["datatype_parameters"])}, "
                remove_last = True
            elif row["django_field_type"] =="CharField":
                info+= f"max_length=1000, "
                remove_last = True
        elif row["django_field_type"] == "ForeignKey":
            info+= f"to='{row["datatype_parameters"]}', on_delete=models.CASCADE, "
            remove_last = True
        elif row["django_field_type"] == "BooleanField":
            if row["datatype_parameters"] != "nan":
                info+= f"default= False, "
            else:
                info+= f"default= {row["datatype_parameters"]}, "
            remove_last = True
            
        # Null
        if row["null_constraint"] != "NOT NULL":
            info += "null=True, blank=True, "
            remove_last = True
        
        else:
            info += "null=False, blank=False, default = '', "
            remove_last = True
        
        # Fechar string
        if remove_last:
            info = info[:-2]
        info += ")\n"
        
    return info


def read_cdm(file_path: str, models_path:str, sheet_name = "Table Summary"):
    try:
        table_summary_df = pd.read_excel(file_path, sheet_name)
        if "table_name" not in table_summary_df.columns:
            print("Error: Required columns 'table_name' is missing in the 'Table Summary' sheet.")
            return
        
        arquivo = open(models_path, "w")
        
        arquivo.write(f"from django.db import models\n\n")
        table_names = table_summary_df["table_name"].dropna().tolist()
        for table_name in table_names:
            try:
                sheet_df = pd.read_excel(file_path, sheet_name=table_name )
                if len(sheet_df) > 0:
                    modle = create_model(sheet_df, table_name)
                    arquivo.write(f"{modle}\n")
                    #print(modle)
            except Exception as e:
                print(f"Error reading sheet '{table_name}' for table '{table_name}': {e}")
        arquivo.close()
    except Exception as e:
        print(f"Error reading 'Table Summary' sheet: {e}")





file_path = "resources/cdm/cdm_fazeconta.xlsx"
models_path = "faz_e_conta/data_hub/models.py"

read_cdm(file_path, models_path)