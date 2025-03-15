import pandas as pd

# CREATE A TABLE IN SQL

def create_table (df, table_name):
    info = ""
    for _, row in df.iterrows():
        if pd.isna(row["datatype_parameters"]):
            info = f"{info}{row["column_name"]} {row["datatype"]}, "
        else:
            info = f"{info}{row["column_name"]} {row["datatype"]}({int(row["datatype_parameters"])}), "
            
            
    return f"CREATE TABLE {table_name} ({info});".replace(", );", ");")


def read_cdm(file_path: str, sheet_name = "Table Summary"):
    try:
        table_summary_df = pd.read_excel(file_path, sheet_name)
        if "table_name" not in table_summary_df.columns:
            print("Error: Required columns 'table_name' is missing in the 'Table Summary' sheet.")
            return
        
        # arquivo = open("cdm_db.txt", "w")
        table_names = table_summary_df["table_name"].dropna().tolist()
        for table_name in table_names:
            try:
                sheet_df = pd.read_excel(file_path, sheet_name=table_name)
                if len(sheet_df) > 0:
                    SQL_quarry = create_table(sheet_df, table_name)
                    # arquivo.write(f"{SQL_quarry}\n")
                    print(f"\n{SQL_quarry}")
            except Exception as e:
                print(f"Error reading sheet '{table_name}' for table '{table_name}': {e}")
        # arquivo.close()
    except Exception as e:
        print(f"Error reading 'Table Summary' sheet: {e}")





file_path = "resources/cdm/cdm_fazeconta.xlsx"
read_cdm(file_path)
