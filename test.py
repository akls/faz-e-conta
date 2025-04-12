# Test file for major changes


import pandas as pd
import datetime
import socket
import os

from django.db import models
import django.utils as du

# Utilitário para IP
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

def get_hostname_ip():
    return socket.gethostbyname(socket.gethostname())

def create_model(df, table_name):
    info = f"""class {table_name.title().replace("_", "")}(models.Model):
    class Meta:
        db_table = '{table_name}'\n"""
    atributes = []

    for _, row in df.iterrows():
        atributes.append(row["column_name"])
        field_declaration = f"    {row['column_name']} = models.{row['django_field_type']}("
        params = []

        if row["auto_id"] == "Yes":
            params.append("primary_key=True")

        if row["django_field_type"] == "CharField":
            max_length = int(row["datatype_parameters"]) if pd.notna(row["datatype_parameters"]) else 255
            params.append(f"max_length={max_length}")

        if row["django_field_type"] == "ForeignKey":
            params.append(f"to='{row['datatype_parameters'].title().replace('_','')}', on_delete=models.CASCADE, db_column='{row['column_name']}'")

        if row["django_field_type"] == "BooleanField":
            default_value = False if pd.isna(row["datatype_parameters"]) else row["datatype_parameters"]
            params.append(f"default={default_value}")

        if row["django_field_type"] == "DateField":
            params.append("default=du.timezone.now")

        if row["null_constraint"] != "NOT NULL":
            params.append("null=True, blank=True")
        else:
            if row["django_field_type"] == "CharField":
                params.append("default=''")

        field_declaration += ", ".join(params) + ")"
        info += field_declaration + "\n"

    info += """
    def __str__(self):
        return f""" + f"self.{atributes[1]} {{self.{atributes[2]}}}, {atributes[0].replace('_', ' ').title()}: {{self.{atributes[0]}}}"""

    return info

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def read_excel_sheet(file_path, sheet_name):
    return pd.read_excel(file_path, sheet_name)

def generate_code():
    file_path = "resources/cdm/cdm_fazeconta.xlsx"
    models_path = "faz_e_conta/data_hub/models.py"
    admin_path = "faz_e_conta/data_hub/admin.py"
    forms_path = "faz_e_conta/data_hub/forms.py"
    form_views_path = models_path.replace("models.py", "auto_gen/auto_gen_form_views.py")
    id_views_path = models_path.replace("models.py", "auto_gen/auto_gen_id_views.py")

    try:
        table_summary_df = read_excel_sheet(file_path, "Table Summary")
        class_list = []

        with open(models_path, "w", encoding="utf-8") as f:
            f.write("from django.db import models\nimport datetime\nimport django.utils as du\n\n")
            for table_name in table_summary_df["table_name"].dropna():
                df = read_excel_sheet(file_path, sheet_name=table_name)
                if not df.empty:
                    model_code = create_model(df, table_name)
                    f.write(f"{model_code}\n")
                    class_list.append(table_name.capitalize())

        generate_admin(admin_path, class_list)
        generate_forms(forms_path, file_path, class_list)
        generate_form_views(form_views_path, class_list)
        generate_html_forms(class_list)
        generate_form_urls(class_list)
        generate_links_html(class_list)
        generate_id_views(id_views_path, class_list)
        generate_id_html(class_list)
        generate_id_urls(class_list)

    except Exception as e:
        print(f"Erro: {e}")

def generate_admin(path, class_list):
    content = "from django.contrib import admin\nfrom .models import *\n\n"
    for cls in class_list:
        content += f"admin.site.register({cls.title().replace('_','')})\n"
    write_file(path, content)

def generate_forms(path, file_path, class_list):
    content = "from django import forms\nfrom .models import *\nfrom .widgets import *\n\n"
    for cls in class_list:
        df = read_excel_sheet(file_path, sheet_name=cls.lower())
        content += f"class {cls}Form(forms.ModelForm):\n"
        content += "    class Meta:\n"
        content += f"        model = {cls.title().replace('_','')}\n"
        content += "        fields = ['" + "', '".join(df["column_name"].tolist()) + "']\n"
        content += "        widgets = default_widget()\n\n"
    write_file(path, content)

def generate_form_views(path, class_list):
    content = "from django.shortcuts import render, redirect\nfrom django.urls import reverse\nfrom ..models import *\nfrom ..forms import *\n\n"
    for cls in class_list:
        lc = cls.lower()
        content += f"def insert_{lc}_view(request):\n"
        content += f"    if request.method == 'POST':\n        form = {cls}Form(request.POST)\n        if form.is_valid():\n            form.save()\n            return redirect(reverse('index'))\n    else:\n        form = {cls}Form()\n    return render(request, 'insert/insert_{lc}.html', {{'form': form}})\n\n"
    write_file(path, content)

def generate_html_forms(class_list):
    style = 'style="display: inline-block; margin-top: 10px; padding: 10px 15px;width: 75%; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;"'
    for cls in class_list:
        form_html_path = f"faz_e_conta/data_hub/templates/insert/insert_{cls.lower()}.html"
        with open(form_html_path, "w", encoding="utf-8") as f:
            f.write("<html lang='pt'>\n<head><meta charset='UTF-8'><title>Inserir {}</title></head>\n<body>\n".format(cls.replace("_", " ").title()))
            f.write("<h1>Inserir {}</h1>\n<form method='post'>\n    {{% csrf_token %}}\n    {{ form.as_p }}\n    <button type='submit'>Inserir</button>\n    <br><a href='javascript:history.back()'>Voltar</a>\n</form>\n</body>\n</html>\n")

def generate_form_urls(class_list):
    path = "faz_e_conta/data_hub/auto_gen/auto_gen_form_url.py"
    content = "from django.urls import path\nfrom .. import views\n\ndef add_form_urlpatterns(urlpatterns):\n"
    for cls in class_list:
        content += f"    urlpatterns.append(path('insert_{cls.lower()}/', views.insert_{cls.lower()}_view, name='insert_{cls.lower()}_view'))\n"
    content += "    return urlpatterns\n"
    write_file(path, content)

def generate_links_html(class_list):
    path = "faz_e_conta/data_hub/templates/links.html"
    table = "<table>\n<tr><th>Inserir</th><th>Ver id1</th></tr>\n"
    style = 'style="display: inline-block; margin-top: 10px; padding: 10px 15px;width: 75%; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;"'
    for cls in class_list:
        table += f"<tr><td><center><a href='{{% url 'insert_{cls.lower()}_view' %}}' {style}>Inserir {cls}</a></center></td><td><center><a href='{{% url '{cls.lower()}_view' {cls.lower()}_id=1 %}}' {style}>Ver {cls} com id 1</a></center></td></tr>\n"
    table += "</table>\n"
    content = table + "{%block links%}\n{%endblock%}\n" + table
    write_file(path, content)

def generate_id_views(path, class_list):
    content = "from django.shortcuts import render\nfrom django.http import HttpResponse\nfrom ..models import *\n\n"
    for cls in class_list:
        model_name = cls.title().replace("_", "")
        content += f"def show_{cls.lower()}_view(request, {cls.lower()}_id):\n"
        content += f"    try:\n        data = {model_name}.objects.get({cls.lower()}_id={cls.lower()}_id)\n    except {model_name}.DoesNotExist:\n        return HttpResponse(f'<h1>{cls} with id={{ {cls.lower()}_id }} not found</h1>')\n    head = [field.name for field in {model_name}.objects.model._meta.fields]\n    data_dict = {{field: getattr(data, field, None) for field in head}}\n    return render(request, 'show/show_{cls.lower()}.html', {{'head': head, 'data_dict': data_dict, 'data': data, 'id': head[0]}})\n\n"
    write_file(path, content)

def generate_id_html(class_list):
    for cls in class_list:
        path = f"faz_e_conta/data_hub/templates/show/show_{cls.lower()}.html"
        content = """{% load custom_filters %}
<!DOCTYPE html>
<html lang='en'>
<head><meta charset='UTF-8'><title>{title} Information</title></head>
<body>
    <h1>{{ data_dict.nome_proprio }} {{ data_dict.apelido }}</h1>
    <table>
        {% for field in head %}
            {% if field != id %}
                <tr align='left'>
                    <th>{{ field|replace:'_id_id, '|replace:'_, '}}</th>
                    {% if data_dict|get_item:field == None %}
                        <td><hr style='border: none; border-top: 3px dashed black;'></td>
                    {% else %}
                        <td>{{ data_dict|get_item:field }}</td>
                    {% endif %}
                </tr>
            {% endif %}
        {% endfor %}
    </table>
    <a href="{% url 'index' %}">Voltar</a>
</body>
</html>
""".replace('{title}', cls.replace('_', ' ').title())
        write_file(path, content)

def generate_id_urls(class_list):
    path = "faz_e_conta/data_hub/auto_gen/auto_gen_show_id_url.py"
    content = "from django.urls import path\nfrom .. import views\n\ndef add_show_id_urlpatterns(urlpatterns):\n"
    for cls in class_list:
        content += f"    urlpatterns.append(path('{cls.lower()}/<int:{cls.lower()}_id>/', views.show_{cls.lower()}_view, name='{cls.lower()}_view'))\n"
    content += "    return urlpatterns\n"
    write_file(path, content)

if __name__ == "__main__":
    generate_code()
    print("Process finished successfully!")
