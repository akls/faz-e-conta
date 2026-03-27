from django.shortcuts import redirect, render, get_object_or_404
from .forms import *
from .models import *
from .auto_gen_form_views import *
from .auto_gen_id_views import *
from django.db.models import Q  # Import Q for dynamic filtering
from django.db.models import F, Value, CharField
from django.db.models.functions import Concat


def starter_page(request):
    return render(request, "show_students.html")




def show_students(request):
    # URL query parameters
    query = request.GET.get("q", "")
    sala_filter = request.GET.get("sala", "")



    # Get alunos in the data base
    alunos = Aluno.objects.all()
    # Apply filters
    if query:
        alunos = alunos.filter(Q(nome_proprio__icontains=query) | Q(apelido__icontains=query) |Q (processo__icontains=query))
    if sala_filter:
        alunos = alunos.filter(Q(sala_id__sala_valencia__icontains=sala_filter) | Q(sala_id__sala_nome__icontains=sala_filter))




    # Render the template with context
    alunoFields = ["aluno_id", "nome_proprio", "apelido", "processo", "numero_documento", "data_admissao", "sala_id__sala_valencia", "sala_id__sala_nome"]
    context = {"alunos": alunos.values(*alunoFields), "salas": Sala.objects.all(), "alunoCount": alunos.count()}
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
    # URL query parameters
    query = request.GET.get("q", "")
    sala_filter = request.GET.get("sala", "")




    # Get guardians
    encarregadosEducacao = ResponsavelEducativo.objects.prefetch_related("aluno_set")
    # Apply search filter
    if query:
        encarregadosEducacao = encarregadosEducacao.filter(nome_proprio__icontains=query)
    # Apply sala_valencia or sala_nome filter
    if sala_filter:
        encarregadosEducacao = encarregadosEducacao.filter(aluno_id__sala_id__sala_nome__icontains=sala_filter)




    # Get alunos per guardian





    # Render the template with context
    fields = ["responsavel_educativo_id", "nome_proprio", "telefone", "email"]
    context = {"guardians": encarregadosEducacao, "salas": Sala.objects.all(), "guardiansCount": encarregadosEducacao.count()}
    return render(request, "show_contactos.html", context)




def show_contactos_details(request, responsavel_id):
    guardian = ResponsavelEducativo.objects.prefetch_related("aluno_set").filter(responsavel_educativo_id=responsavel_id)[0]

    context = {"guardian": guardian}
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

    # Base queryset for rooms, ordered alphabetically
    salas = Sala.objects.all().order_by('sala_valencia', 'sala_nome')

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
    aluno = Aluno.objects.select_related("sala_id", "responsavel_educativo_id").filter(aluno_id=aluno_id)[0]

    context = {"aluno": aluno}
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