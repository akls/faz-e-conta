# Test file for major changes


import pandas as pd
import datetime
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

def create_model(df, table_name):
    # Function to create models

    # Start the class definition
    info = f"""class {table_name.title().replace("_","")}(models.Model):
    class Meta:
        db_table = '{table_name}'\n"""
    atributes = []
    
    # Iterate over each row in the dataframe to define fields
    for _, row in df.iterrows():
        atributes.append(row["column_name"])
        field_declaration = f"    {row['column_name']} = models.{row['django_field_type']}("
        params = []
        
        # Auto ID field
        if row["auto_id"] == "Yes":
            params.append("primary_key=True")
        
        # If CharField, check for max_length
        if row["django_field_type"] == "CharField":
            max_length = int(row["datatype_parameters"]) if pd.notna(row["datatype_parameters"]) else 255
            params.append(f"max_length={max_length}")

        # If ForeignKey, set correctly
        if row["django_field_type"] == "ForeignKey":
            params.append(f"to='{row['datatype_parameters'].title().replace("_","")}', on_delete=models.CASCADE")

        # If BooleanField, set default correctly
        if row["django_field_type"] == "BooleanField":
            default_value = False if pd.isna(row["datatype_parameters"]) else row["datatype_parameters"]
            params.append(f"default={default_value}")

        # If DateField, correct invalid default
        if row["django_field_type"] == "DateField":
            params.append("default= du.timezone.now")

        # NULL constraints
        if row["null_constraint"] != "NOT NULL":
            params.append("null=True, blank=True")
        else:
            if row["django_field_type"] == "CharField":
                params.append("default=''")
            elif row["django_field_type"] == "BooleanField":
                params.append("default=False")
        
        # Construct the final field declaration line
        field_declaration += ", ".join(params) + ")"
        info += field_declaration + "\n"
    
    # Add the __str__ method for the model
    info += """
    def __str__(self):
        return f"{""" + f"self.{atributes[1]}" + "} {self. " + f"{atributes[2]}" + "}, " + f"{atributes[0].replace("_", " ").title()}: " + "{" + f"self.{atributes[0]}" + '}"\n'
    
    return info


def read_cdm(sheet_name="Table Summary"):
    file_path = "resources/cdm/cdm_fazeconta.xlsx"
    models_path = "faz_e_conta/data_hub/models.py"
    admin_path = "faz_e_conta/data_hub/admin.py"
    forms_path = "faz_e_conta/data_hub/forms.py"
    form_views_path = models_path.replace("models.py", "auto_gen_form_views.py")
    id_views_path = models_path.replace("models.py", "auto_gen_id_views.py")

    try:
        table_summary_df = pd.read_excel(file_path, sheet_name)
        if "table_name" not in table_summary_df.columns:
            print("Erro: A coluna 'table_name' não está presente na planilha 'Table Summary'.")
            return

        class_list = generate_models(table_summary_df, file_path, models_path)
        generate_admin(class_list, admin_path)
        generate_forms(class_list, file_path, forms_path)
        generate_form_views(class_list, form_views_path)
        generate_html_forms(class_list)
        generate_form_urls(class_list)
        generate_links_html(class_list)
        generate_id_views(class_list, id_views_path)
        generate_show_id_urls(class_list)
        print("Process finished successfully!")
    except Exception as e:
        print(f"Erro ao ler a planilha 'Table Summary': {e}")
    
    
def generate_models(table_summary_df, file_path, models_path):
    print("Creating models on models.py...")
    class_list = []
    
    with open(models_path, "w", encoding="utf-8") as arquivo:
        arquivo.write("from django.db import models\nimport datetime\nimport django.utils as du\n\n")
        
        for table_name in table_summary_df["table_name"].dropna().tolist():
            try:
                sheet_df = pd.read_excel(file_path, sheet_name=table_name)
                if not sheet_df.empty:
                    model_code = create_model(sheet_df, table_name)
                    arquivo.write(f"{model_code}\n")
                    class_list.append(table_name.capitalize())
            except Exception as e:
                print(f"Erro ao ler a planilha '{table_name}': {e}")
    
    return class_list


def generate_admin(class_list, admin_path):
    print("Adding classes to admin.py...")
    with open(admin_path, "w", encoding="utf-8") as arquivo:
        arquivo.write("from django.contrib import admin\n")
        arquivo.write("from .models import *\n\n")
        for table_name in class_list:
            arquivo.write(f"admin.site.register({table_name.title().replace('_','')})\n")


def generate_forms(class_list, file_path, forms_path):
    print("Adding classes to forms.py...")
    with open(forms_path, "w", encoding="utf-8") as arquivo:
        arquivo.write("from django import forms\nfrom .models import *\nfrom .widgets import *\n\n")
        for table_name in class_list:
            sheet_df = pd.read_excel(file_path, sheet_name=table_name.lower())
            arquivo.write(f"class {table_name}Form(forms.ModelForm):\n")
            arquivo.write("    class Meta:\n")
            arquivo.write(f"        model = {table_name.title().replace('_','')}\n")
            arquivo.write("        fields = ['" + "', '".join(sheet_df["column_name"].tolist()) + "']\n\n")
            arquivo.write(f"        widgets = {table_name}_widget()\n\n")


def generate_form_views(class_list, form_views_path):
    print("Adding views to form_views.py...")
    with open(form_views_path, "w", encoding="utf-8") as arquivo:
        arquivo.write("from django.shortcuts import render, redirect\nfrom django.urls import reverse\nfrom .models import *\nfrom .forms import *\n\n")
        for table_name in class_list:
            arquivo.write(f"def insert_{table_name.lower()}_view(request):\n")
            arquivo.write("    if request.method == 'POST':\n")
            arquivo.write(f"        form = {table_name}Form(request.POST)\n")
            arquivo.write("        if form.is_valid():\n")
            arquivo.write("            form.save()\n")
            arquivo.write("            return redirect(reverse('index'))\n")
            arquivo.write("    else:\n")
            arquivo.write(f"        form = {table_name}Form()\n")
            arquivo.write(f"    return render(request, 'insert_{table_name.lower()}.html', {{'form': form}})\n\n")


def generate_html_forms(class_list):
    print("Creating HTML files for forms...")
    for table_name in class_list:
        form_html_path = f"faz_e_conta/data_hub/templates/insert_{table_name.lower()}.html"
        with open(form_html_path, "w", encoding="utf-8") as arquivo:
            arquivo.write("<html>\n<head>\n    <title>Inserir {table_name}</title>\n</head>\n<body>\n")
            arquivo.write("    <h1>Inserir {table_name}</h1>\n")
            arquivo.write("    <form method='post'>\n        {% csrf_token %}\n        {{ form.as_p }}\n        <button type='submit'>Inserir</button>\n")
            arquivo.write("        <a href=\"{% url 'index' %}\">Voltar</a>\n    </form>\n</body>\n</html>\n")


def generate_form_urls(class_list):
    print("Adding classes to form_url.py...")
    with open("faz_e_conta/data_hub/auto_gen_form_url.py", "w", encoding="utf-8") as arquivo:
        arquivo.write("from django.urls import path\nfrom . import views\n\n")
        arquivo.write("def add_form_urlpatterns(urlpatterns):\n")
        for table_name in class_list:
            arquivo.write(f"    urlpatterns.append(path('insert_{table_name.lower()}/', views.insert_{table_name.lower()}_view, name='insert_{table_name.lower()}_view'))\n")
        
        arquivo.write("return urlpatterns\n")


def generate_links_html(class_list):
    print("Adding links to links.html...")
    with open("faz_e_conta/data_hub/templates/links.html", "w", encoding="utf-8") as arquivo:
        for table_name in class_list:
            arquivo.write(f"<a href=\"{{% url 'insert_{table_name.lower()}_view' %}}\">Inserir {table_name}</a><br>\n")


def generate_id_views(class_list, id_views_path):
    print("Adding views to id_views.py...")
    with open(id_views_path, "w", encoding="utf-8") as arquivo:
        for table_name in class_list:
            arquivo.write(f"def show_{table_name.lower()}_view(request, {table_name.lower()}_id):\n")
            arquivo.write("    return render(request, 'show_{table_name.lower()}.html', {})\n\n")


def generate_show_id_urls(class_list):
    print("Adding urls to id_views.py...")
    with open("faz_e_conta/data_hub/auto_gen_show_id_url.py", "w", encoding="utf-8") as arquivo:
        for table_name in class_list:
            arquivo.write(f"urlpatterns.append(path('{table_name.lower()}/<int:id>/', views.show_{table_name.lower()}_view))\n")


# Executar o gerador
read_cdm()

#
# python manage.py runserver 0.0.0.0:8000 
print("URL to external axcess:")
print("https://"+IPAddr+":8000/")