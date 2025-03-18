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

# Function to read the CDM and create the models automatically
def read_cdm(sheet_name="Table Summary"):
# File paths
    file_path = "resources/cdm/cdm_fazeconta.xlsx"
    models_path = "faz_e_conta/data_hub/models.py"
    admin_path = "faz_e_conta/data_hub/admin.py"
    forms_path = "faz_e_conta/data_hub/forms.py"
    form_views_path = models_path.replace("models.py", "auto_gen_form_views.py")
    id_views_path = models_path.replace("models.py", "auto_gen_id_views.py")
    
    try:

# Create models on models.py
        table_summary_df = pd.read_excel(file_path, sheet_name)
        class_list = []
        print("Creating models on models.py...")
        
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
        
# Add classes to admin.py
        print("Adding classes to admin.py...")

        with open(admin_path, "w", encoding="utf-8") as arquivo:
            arquivo.write("from django.contrib import admin\n")
            arquivo.write(f"from .models import *\n\n")
            arquivo.write("# Register your models here.\n\n")
            for table_name in class_list:
                arquivo.write(f"admin.site.register({table_name.title().replace("_","")})\n")
        
# Add classes to forms.py 
        print("Adding classes to forms.py...")        

        with open(forms_path, "w", encoding="utf-8") as arquivo:
            arquivo.write("from django import forms\n")
            arquivo.write(f"from .models import *\n")
            arquivo.write("from .widgets import *\n")
            arquivo.write("\n")
            for table_name in class_list:
                sheet_df = pd.read_excel(file_path, sheet_name=table_name.lower())
                arquivo.write(f"class {table_name}Form(forms.ModelForm):\n")
                arquivo.write("    class Meta:\n")
                arquivo.write(f"        model = {table_name.title().replace("_","")}\n")
                arquivo.write("        fields = ['" + "', '".join(sheet_df["column_name"].tolist()) + "']\n\n")
                arquivo.write("        # Adiciona atributos aos campos do formulário\n")
                arquivo.write(f"        widgets = {table_name}_widget()\n\n")
        
# Add views to form_views.py
        print("Adding views to form_views.py...")        

        with open(form_views_path, "w", encoding="utf-8") as arquivo:
            arquivo.write("from django.shortcuts import render, redirect\n")
            arquivo.write("from django.urls import reverse\n")
            arquivo.write(f"from .models import *\n")
            arquivo.write(f"from .forms import *\n\n")
            
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

# Create HTML files for forms
        print("Creating HTML files for forms...")

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
    
# Add classes to form_url.py

        print("Adding classes to form_url.py...")
        
        with open("faz_e_conta/data_hub/auto_gen_form_url.py", "w", encoding="utf-8") as arquivo:
            arquivo.write("from django.urls import path\n")
            arquivo.write("from . import views\n\n")
            arquivo.write("def add_form_urlpatterns(urlpatterns):\n")
            for table_name in class_list:
                arquivo.write(f"    urlpatterns.append(path('insert_{table_name.lower()}/', views.insert_{table_name.lower()}_view, name='insert_{table_name.lower()}_view'))\n")
            arquivo.write("\n    return urlpatterns\n")

# Add links to links.html
        print("Adding links to links.html...")
        table = ""
        with open("faz_e_conta/data_hub/templates/links.html", "w", encoding="utf-8") as arquivo:
            style = 'style="display: inline-block; margin-top: 10px; padding: 10px 15px;width: 75%; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;"'
            table += "<table>\n"
            table += ("    <tr>\n")
            table += (f"        <th>Inserir</th>\n")
            table += (f"        <th>Ver id1</th>\n")
            table += ("    </tr>\n")
            for table_name in class_list:
                table += ("    <tr>\n")
                table += (f"        <td><center><a href=\"{{% url 'insert_{table_name.lower()}_view' %}}\" {style}>Inserir {table_name.replace('_', ' ').title()}</a></center></td>\n")
                table += (f"        <td><center><a href=\"{{% url '{table_name.lower()}_view' {table_name.lower()}_id=1 %}}\" {style}>Ver {table_name.replace('_', ' ').title()} com id 1</a></center></td>\n")
                table += ("    </tr>\n")
            table += "</table>\n"
            arquivo.write(table)
            arquivo.write("{%block links%}\n")
            arquivo.write("{%endblock%}\n")
            arquivo.write(table)
            
# Add views to id_views.py
        print("Adding views to id_views.py...")
        
        with open(id_views_path, "w", encoding="utf-8") as arquivo:
            arquivo.write("from django.shortcuts import render, redirect\n")
            arquivo.write("from django.urls import reverse\n")
            arquivo.write(f"from .models import *\n")
            arquivo.write(f"from .forms import *\n\n")
            arquivo.write(f"from django.http import Http404\n")
            arquivo.write("from django.http import HttpResponse\n\n")

            for table_name in class_list:
                arquivo.write(f"def show_{table_name.lower()}_view(request, {table_name.lower()}_id):\n")
                arquivo.write(f"    try:\n")
                arquivo.write(f"        data = {table_name.title().replace("_","")}.objects.get({table_name.lower()}_id={table_name.lower()}_id)  # Verifique se 'id' é o nome correto do campo\n")
                arquivo.write(f"    except {table_name.title().replace("_","")}.DoesNotExist:\n")
                arquivo.write(f"        return HttpResponse(f'<h1>{table_name.replace("_", " ").title()} with id= " + '{' + f"{table_name.lower()}_id" + "}" + " not found</h1><a href=\"/\">Voltar para o índice</a>')\n")
                arquivo.write(f"    head = [field.name.replace('_id','_id_id') for field in {table_name.title().replace("_","")}._meta.fields]\n")
                arquivo.write(f'''
    for i in range(1, len(head)):
        if head[i].endswith('_id_id'):
            related_model_name = head[i].replace('_id_id', '')
            related_model = globals()[related_model_name.capitalize()]
            related_instance = related_model.objects.get(pk=data.__dict__.get(head[i]))
            data.__dict__[head[i]] = related_instance\n''')
                arquivo.write(f"    data_dict = {{head[i]: data.__dict__.get(head[i], None) for i in range(1, len(head))}}\n\n")
                arquivo.write(f"    return render(request, 'show_{table_name.lower()}.html', {{'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]}})\n\n")

# Add HTML files for views by id
        print("Adding HTML files for views by id...")
        
        for table_name in class_list:
            view_html_path = f"faz_e_conta/data_hub/templates/show_{table_name.lower()}.html"
            with open(view_html_path, "w", encoding="utf-8") as arquivo:
                arquivo.write("{% load custom_filters %}\n")
                arquivo.write("<!DOCTYPE html>\n")
                arquivo.write("<html lang='en'>\n")
                arquivo.write("<head>\n")
                arquivo.write("    <meta charset='UTF-8'>\n")
                arquivo.write("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
                arquivo.write(f"    <title>{table_name.replace('_', ' ').title()} Information</title>\n")
                arquivo.write("</head>\n")
                arquivo.write("<body>\n")
                arquivo.write(f"    <h1>{{{{ data_dict.nome_proprio }}}} {{{{ data_dict.apelido }}}}</h1>\n")
                arquivo.write("    <table>\n")
                arquivo.write("        {% for field in head %}\n")
                arquivo.write("            {% if field != id %}\n")
                arquivo.write("                <tr align='left'>\n")
                arquivo.write("                    <th>{{ field|replace:'_id_id, '|replace:'_, '}}</th>\n")
                arquivo.write("                    {% if data_dict|get_item:field == None %}\n")
                arquivo.write("                        <td>\n")
                arquivo.write("                            <hr style='border: none; border-top: 3px dashed black;'>\n")
                arquivo.write("                        </td>\n")
                arquivo.write("                    {% else %}\n")
                arquivo.write("                        <td>{{ data_dict|get_item:field }}</td>\n")
                arquivo.write("                    {% endif %}\n")
                arquivo.write("                </tr>\n")
                arquivo.write("            {% endif %}\n")
                arquivo.write("        {% endfor %}\n")
                arquivo.write("    </table>\n")
                arquivo.write("    <a href=\"{% url 'show_students' %}\">Voltar</a>\n")
                arquivo.write("</body>\n")
                arquivo.write("</html>\n")

# Add urls to id_views.py
        print("Adding urls to id_views.py...")
        
        with open("faz_e_conta/data_hub/auto_gen_show_id_url.py", "w", encoding="utf-8") as arquivo:
            arquivo.write("from django.urls import path\n")
            arquivo.write("from . import views\n\n")
            arquivo.write("def add_show_id_urlpatterns(urlpatterns):\n")
            for table_name in class_list:
                arquivo.write(f"    urlpatterns.append(path('{table_name.lower()}/<int:{table_name.lower()}_id>/', views.show_{table_name.lower()}_view, name='{table_name.lower()}_view'))\n")
            arquivo.write("\n    return urlpatterns\n")

# End
    except Exception as e:
        print(f"{e}")


# Executar o gerador
read_cdm()
print("Process finished successfully!")


# python manage.py runserver 0.0.0.0:8000 
#print("URL to external axcess:")
#print("https://"+IPAddr+":8000/")