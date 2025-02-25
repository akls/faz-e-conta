import pandas as pd
import datetime

# Automatizar criação view by id     



# Função para criar os modelos
def create_model(df, table_name):
    info = f"""class {table_name.capitalize()}(models.Model):
    class Meta:
        db_table = '{table_name}'\n"""

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
def read_cdm(file_path: str, models_path: str, admin_path: str, forms_path: str, form_views_path:str , sheet_name="Table Summary"):
    try:

# criar models.py
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
        print("A criar admin para os modelos...")

        with open(admin_path, "w", encoding="utf-8") as arquivo:
            arquivo.write("from django.contrib import admin\n")
            arquivo.write(f"from .models import {', '.join(class_list)}\n\n")
            arquivo.write("# Register your models here.\n\n")
            for table_name in class_list:
                arquivo.write(f"admin.site.register({table_name})\n")
        
# Adicionar as classes ao arquivo forms.py
        print("A criar formulários para os modelos...")        

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
        
# Adicionar as views ao arquivo form_views.py
        print("A criar views para os formulários...")        

        with open(form_views_path, "w", encoding="utf-8") as arquivo:
            arquivo.write("from django.shortcuts import render, redirect\n")
            arquivo.write("from django.urls import reverse\n")
            arquivo.write(f"from .models import {', '.join(class_list)}\n")
            arquivo.write(f"from .forms import {', '.join([f'{table_name}Form' for table_name in class_list])}\n\n")
            
            for table_name in class_list:
                arquivo.write(f"def insert_{table_name.lower()}_view(request):\n")
                arquivo.write(f"    if request.method == 'POST':\n")
                arquivo.write(f"        form = {table_name}Form(request.POST)\n")
                arquivo.write(f"        if form.is_valid():\n")
                arquivo.write(f"            form.save()\n")
                arquivo.write(f"            return redirect(reverse('index'))\n")
                arquivo.write(f"    else:\n")
                arquivo.write(f"        form = {table_name}Form()\n")
                arquivo.write(f"    return render(request, 'insert_{table_name.lower()}.html', {{'form': form}})\n\n")

# Criar paginas html para os forms
        print("A criar páginas html para os formulários...")

        for table_name in class_list:
            form_html_path = f"faz_e_conta/data_hub/templates/insert_{table_name.lower()}.html"
            with open(form_html_path, "w", encoding="utf-8") as arquivo:
                arquivo.write("<html lang='pt'>\n")
                arquivo.write("<head>\n")
                arquivo.write("    <meta charset='UTF-8'>\n")
                arquivo.write("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
                arquivo.write(f"    <title>Inserir {table_name.replace("_", " ").title()}</title>\n")
                arquivo.write("    <style>\n")
                arquivo.write("        body {\n")
                arquivo.write("            font-family: Arial, sans-serif;\n")
                arquivo.write("            background-color: #f4f4f4;\n")
                arquivo.write("            display: flex;\n")
                arquivo.write("            flex-direction: column;\n")
                arquivo.write("            justify-content: flex-start;\n")
                arquivo.write("            align-items: center;\n")
                arquivo.write("            height: 100vh;\n")
                arquivo.write("            margin: 20px 0;\n")
                arquivo.write("            overflow-y: auto;\n")
                arquivo.write("        }\n")
                arquivo.write("\n")
                arquivo.write("        form {\n")
                arquivo.write("            background: white;\n")
                arquivo.write("            padding: 20px;\n")
                arquivo.write("            border-radius: 8px;\n")
                arquivo.write("            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);\n")
                arquivo.write("            width: 300px;\n")
                arquivo.write("            text-align: center;\n")
                arquivo.write("        }\n")
                arquivo.write("\n")
                arquivo.write("        h1 {\n")
                arquivo.write("            text-align: center;\n")
                arquivo.write("            color: #333;\n")
                arquivo.write("        }\n")
                arquivo.write("\n")
                arquivo.write("        button {\n")
                arquivo.write("            width: 100%;\n")
                arquivo.write("            padding: 10px;\n")
                arquivo.write("            background: #007bff;\n")
                arquivo.write("            color: white;\n")
                arquivo.write("            border: none;\n")
                arquivo.write("            border-radius: 5px;\n")
                arquivo.write("            cursor: pointer;\n")
                arquivo.write("            font-size: 16px;\n")
                arquivo.write("            transition: background 0.3s ease;\n")
                arquivo.write("        }\n")
                arquivo.write("\n")
                arquivo.write("        button:hover {\n")
                arquivo.write("            background: #0056b3;\n")
                arquivo.write("        }\n")
                arquivo.write("\n")
                arquivo.write("        a {\n")
                arquivo.write("            display: block;\n")
                arquivo.write("            text-align: center;\n")
                arquivo.write("            margin-top: 10px;\n")
                arquivo.write("            text-decoration: none;\n")
                arquivo.write("            color: #007bff;\n")
                arquivo.write("            font-size: 16px;\n")
                arquivo.write("        }\n")
                arquivo.write("\n")
                arquivo.write("        a:hover {\n")
                arquivo.write("            text-decoration: underline;\n")
                arquivo.write("        }\n")
                arquivo.write("\n")
                arquivo.write("        input, select, textarea {\n")
                arquivo.write("            width: 90%;\n")
                arquivo.write("            padding: 8px;\n")
                arquivo.write("            margin: 8px 0;\n")
                arquivo.write("            border: 1px solid #ccc;\n")
                arquivo.write("            border-radius: 4px;\n")
                arquivo.write("        }\n")
                arquivo.write("\n")
                arquivo.write("        label {\n")
                arquivo.write("            font-weight: bold;\n")
                arquivo.write("            color: #555;\n")
                arquivo.write("        }\n")
                arquivo.write("    </style>\n")
                arquivo.write("</head>\n")
                arquivo.write("<body>\n")
                arquivo.write(f"    <h1>Inserir {table_name}</h1>\n")
                arquivo.write("    <form method='post'>\n")
                arquivo.write("        {% csrf_token %}\n")
                arquivo.write("        {{ form.as_p }}\n")
                arquivo.write("        <button type='submit'>Inserir</button>\n")
                arquivo.write("        <a href=\"{% url 'index' %}\">Voltar</a>\n")
                arquivo.write("    </form>\n")
                arquivo.write("</body>\n")
                arquivo.write("</html>\n")
    
# Adicionar as classes ao arquivo url_tools.py
        print("A criar urls para os formulários...")
        
        with open("faz_e_conta/data_hub/url_tools.py", "w", encoding="utf-8") as arquivo:
            arquivo.write("from django.urls import path\n")
            arquivo.write("from . import views\n\n")
            arquivo.write("def add_urlpatterns(urlpatterns):\n")
            for table_name in class_list:
                arquivo.write(f"    urlpatterns.append(path('insert_{table_name.lower()}/', views.insert_{table_name.lower()}_view, name='insert_{table_name.lower()}_view'))\n")
            arquivo.write("\n    return urlpatterns\n")

# Adicionar os links ao arquivo links.html
        print("A criar links para os formulários...")
        
        with open("faz_e_conta/data_hub/templates/links.html", "w", encoding="utf-8") as arquivo:
            
            arquivo.write("{% block links %}\n")
            arquivo.write("    <h1>Links:</h1>\n")
            style = 'style="display: inline-block; margin-top: 10px; padding: 10px 15px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;"'
            for table_name in class_list:
                arquivo.write(f"    <a href=\"{{% url 'insert_{table_name.lower()}_view' %}}\" {style}>Inserir {table_name.replace('_', ' ').title()}</a><br>\n")
            arquivo.write("{% endblock %}\n")

# End
    except Exception as e:
        print(f"Erro ao ler a planilha 'Table Summary': {e}")

# Caminhos dos arquivos
file_path = "resources/cdm/cdm_fazeconta.xlsx"
models_path = "faz_e_conta/data_hub/models.py"
admin_path = "faz_e_conta/data_hub/admin.py"
forms_path = "faz_e_conta/data_hub/forms.py"
form_views_path = models_path.replace("models.py", "form_views.py")

# Executar o gerador
read_cdm(file_path, models_path, admin_path, forms_path, form_views_path)
