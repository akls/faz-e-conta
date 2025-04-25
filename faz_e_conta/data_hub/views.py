from django.shortcuts import redirect, render, get_object_or_404
from .forms import *
from .models import *
from .auto_gen_form_views import *
from .auto_gen_id_views import *
from django.db.models import Q  # Import Q for dynamic filtering
from django.db.models import F, Value, CharField
from django.db.models.functions import Concat


def starter_page(request):
    return render(request, "starter_page.html")

def show_students(request):
    query = request.GET.get("q", "")  # Get search query from the URL
    sala_filter = request.GET.get("sala", "")  # Get sala filter from the URL

    # Base queryset
    data = Aluno.objects.select_related('sala_id').all()

    # Apply search filter
    if query:
        data = data.filter(
            Q(nome_proprio__icontains=query) | 
            Q(apelido__icontains=query) | 
            Q(processo__icontains=query)
        )

    # Apply sala_valencia or sala_nome filter
    if sala_filter:
        data = data.filter(
            Q(sala_id__sala_valencia__icontains=sala_filter) |
            Q(sala_id__sala_nome__icontains=sala_filter)
        )

    # Define the fields to display
    head = ["aluno_id", "nome_proprio", "apelido", "processo", "numero_documento", "data_admissao", "sala_id__sala_valencia", "sala_id__sala_nome"]
    data_dict = list(data.values(*head))

    # Get unique sala_valencia and sala_nome values for the dropdown
    salas = Sala.objects.values_list("sala_valencia", flat=True).distinct()
    sala_nomes = Sala.objects.values_list("sala_nome", flat=True).distinct()

    # Render the template with context
    context = {
        "head": head,
        "data_dict": data_dict,
        "id": head[0],
        "query": query,
        "sala_filter": sala_filter,
        "salas": salas,
        "sala_nomes": sala_nomes,
    }
    return render(request, "show_students.html", context)

def show_financas(request):
    query = request.GET.get("q", "")  # Get search query from the URL

    # Base queryset
    data = AlunoFinancas.objects.all()

    # Apply search filter by student ID
    if query:
        data = data.filter(aluno_id__aluno_id__icontains=query)

    # Define the fields to display
    head = ["ano_letivo", "despesa_anual", "rendim_líquido", "aluno_id__nome_proprio", "aluno_id__apelido", "aluno_id__numero_documento"]
    data_dict = list(data.values(*head))

    # Render the template with context
    context = {
        "head": head,
        "data_dict": data_dict,
        "id": "aluno_id__nome_proprio",  # Use student name as identifier
        "query": query,
    }
    return render(request, "show_aluno_financas.html", context)

def show_contactos(request):
    query = request.GET.get("q", "")  # Get search query from the URL
    sala_filter = request.GET.get("sala", "")  # Get sala filter from the URL

    # Base queryset with annotation for full name
    data = Aluno.objects.select_related('responsaveleducativo', 'sala_id').annotate(
        responsavel_nome_completo=Concat(
            F('responsaveleducativo__nome_proprio'),
            Value(' '),
            F('responsaveleducativo__apelido'),
            output_field=CharField()
        )
    )

    # Apply search filter
    if query:
        data = data.filter(
            Q(nome_proprio__icontains=query) |
            Q(apelido__icontains=query) |
            Q(responsavel_nome_completo__icontains=query)
        )

# Apply sala_valencia or sala_nome filter
    if sala_filter:
        data = data.filter(
            Q(sala_id__sala_valencia__icontains=sala_filter) |
            Q(sala_id__sala_nome__icontains=sala_filter)
        )

    # Define the fields to display
    head = ["nome_proprio", "apelido", "responsavel_nome_completo", "responsaveleducativo__telefone", "responsaveleducativo__email", "sala_id__sala_valencia", "sala_id__sala_nome"]
    data_dict = list(data.values(*head))

    # Get unique sala_valencia and sala_nome values for the dropdown
    salas = Sala.objects.values_list("sala_valencia", flat=True).distinct()
    sala_nomes = Sala.objects.values_list("sala_nome", flat=True).distinct()

    # Render the template with context
    context = {
        "head": head,
        "data_dict": data_dict,
        "id": "nome_proprio",  # Use student name as identifier
        "query": query,
        "sala_filter": sala_filter,
        "salas": salas,
        "sala_nomes": sala_nomes,
    }
    return render(request, "show_contactos.html", context)

def show_contactos_details(request, responsavel_id):
    responsavel = get_object_or_404(ResponsavelEducativo, pk=responsavel_id)
    aluno = responsavel.aluno_id

    context = {
        "responsavel": responsavel,
        "aluno": aluno,
    }
    return render(request, "show_contactos_details.html", context)

def show_aluno(request):
    query = request.GET.get("q", "")  # Get search query from the URL
    sala_filter = request.GET.get("sala", "")  # Get sala filter from the URL

    # Base queryset
    data = Aluno.objects.all()

    # Apply search filter
    if query:
        data = data.filter(
            Q(nome_proprio__icontains=query) |
            Q(apelido__icontains=query)
        )

    # Apply sala_valencia filter
    if sala_filter:
        data = data.filter(sala_id__sala_valencia__icontains=sala_filter)

    # Define the fields to display
    head = ["nome_proprio", "apelido", "processo", "sala_id__sala_valencia"]
    data_dict = list(data.values(*head))

    # Get unique sala_valencia values for the dropdown
    salas = Sala.objects.values_list("sala_valencia", flat=True).distinct()

    # Render the template with context
    context = {
        "head": head,
        "data_dict": data_dict,
        "id": "nome_proprio",  # Use student name as identifier
        "query": query,
        "sala_filter": sala_filter,
        "salas": salas,
    }
    return render(request, "show_aluno.html", context)

def show_salas(request):
    query_valencia = request.GET.get("valencia", "")  # Filter by valencia
    query_room = request.GET.get("room", "")  # Filter by room

    # Base queryset for rooms
    salas = Sala.objects.all()

    # Apply filters
    if query_valencia:
        salas = salas.filter(sala_valencia__icontains=query_valencia)
    if query_room:
        salas = salas.filter(sala_nome__icontains=query_room)

    # Get unique valencias and room names for dropdown filters
    valencias = Sala.objects.values_list("sala_valencia", flat=True).distinct()
    room_names = Sala.objects.values_list("sala_nome", flat=True).distinct()

    # Get all students
    students = Aluno.objects.all()

    if request.method == "POST":
        # Assign students to a room
        selected_room_id = request.POST.get("room_id")
        selected_students = request.POST.getlist("students")

        if selected_room_id and selected_students:
            room = Sala.objects.get(id=selected_room_id)
            Aluno.objects.filter(id__in=selected_students).update(sala_id=room)

    context = {
        "salas": salas,
        "valencias": valencias,
        "room_names": room_names,
        "students": students,
        "query_valencia": query_valencia,
        "query_room": query_room,
    }
    return render(request, "show_sala.html", context)

def show_despesas(request):
    start_date = request.GET.get("start_date", "")  # Data inicial
    end_date = request.GET.get("end_date", "")  # Data final

    # Base queryset para despesas variáveis
    despesas = DespesasVariavel.objects.all()

    # Aplicar filtros de data, se fornecidos
    if start_date and end_date:
        despesas = despesas.filter(data__range=[start_date, end_date])

    # Definir os campos a exibir
    head = ["despvar_id","fatura", "pagamento", "data", "produto", "valor"]
    data_dict = list(despesas.values(*head))

    # Renderizar o template com o contexto
    context = {
        "head": head,
        "data_dict": data_dict,
        "start_date": start_date,
        "end_date": end_date,
    }
    return render(request, "show_despesa.html", context)

def show_student_details(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    responsavel = ResponsavelEducativo.objects.filter(aluno_id=aluno).first()
    sala = aluno.sala_id

    context = {
        "aluno": aluno,
        "responsavel": responsavel,
        "sala": sala,
    }
    return render(request, "show_student_details.html", context)

def edit_student(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    if request.method == "POST":
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('show_student_details', aluno_id=aluno_id)
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'edit_student.html', {'form': form})

def edit_responsavel_educativo(request, responsavel_id):
    responsavel = get_object_or_404(ResponsavelEducativo, pk=responsavel_id)
    if request.method == "POST":
        form = Responsavel_educativoForm(request.POST, instance=responsavel)  # Use the correct form name
        if form.is_valid():
            form.save()
            return redirect('show_contactos')
        else:
            print(form.errors)  # Debugging: Print form errors
    else:
        form = Responsavel_educativoForm(instance=responsavel)  # Use the correct form name
    return render(request, 'edit_responsavel_educativo.html', {'form': form})

def insert_aluno_view(request):
    if request.method == "POST":
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('show_students')  # Redirect to the students list page
        else:
            print(form.errors)  # Debugging: Print form errors
    else:
        form = AlunoForm()
    return render(request, 'insert_aluno.html', {'form': form})

def insert_responsavel_educativo_view(request):
    if request.method == "POST":
        form = Responsavel_educativoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_contactos')  # Redirect to the contactos list page
        else:
            print(form.errors)  # Debugging: Print form errors
    else:
        form = Responsavel_educativoForm()
    return render(request, 'insert_responsavel_educativo.html', {'form': form})

def insert_funcionario_view(request):
    if request.method == "POST":
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('starter_page')  # Redirect to the starter page
        else:
            print(form.errors)  # Debugging: Print form errors
    else:
        form = FuncionarioForm()
    return render(request, 'insert_funcionario.html', {'form': form})