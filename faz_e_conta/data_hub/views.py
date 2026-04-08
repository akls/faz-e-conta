
from _datetime import datetime as dt, timezone
from decimal import Decimal

from django.shortcuts import redirect, render, get_object_or_404
from .auto_gen_id_views import *
from django.db.models import Q
from django.utils import timezone



def starter_page(request):
    return render(request, "starter_page.html")




def show_students(request):
    # URL query parameters
    query = request.GET.get("q", "")
    sala_filter = request.GET.get("sala", "")



    # Get alunos in the data base
    alunos = Aluno.objects.all()
    # Apply filters
    if query:
        alunos = alunos.filter(Q(nome_proprio__icontains=query) | Q(apelido__icontains=query))
    if sala_filter:
        alunos = alunos.filter(Q(sala_id__sala_valencia__icontains=sala_filter) | Q(sala_id__sala_nome__icontains=sala_filter))




    # Render the template with context
    alunoFields = ["aluno_id", "nome_proprio", "apelido", "processo", "numero_documento", "data_admissao", "sala_id__sala_valencia", "sala_id__sala_nome"]
    context = {"alunos": alunos.values(*alunoFields), "salas": Sala.objects.all(), "alunoCount": alunos.count(), "filtersValue": {"sala": sala_filter, "name": query}}
    return render(request, "show_students.html", context)




def show_financas(request):

    # Verefica se o request é um post
    if request.method == "POST" and 'mensalidadeFinal' in request.POST:

        now = timezone.now()
        # Calcular mensalidades
        for financa in AlunoFinancas.objects.all():

            # Calculo da perc
            RMM = (financa.rendim_líquido - financa.despesa_anual) / (12 * financa.agregado)
            RMMG = float(ConfigIpss.objects.all().get(Q(key="RMMG") & Q(active_flag=1)).value)
            percParaEscaloes = (RMM / RMMG) * 100

            # Saber o escalao e a percentagem para aplicar a capital
            escaloes = EscaloesRendimento.objects.all()
            escalaoDoAluno = ""
            percParaAplicarCapital = 0.0
            for escalao in escaloes:
                if escalao.perc_rend_per_capita_max is None and percParaEscaloes >= escalao.perc_rend_per_capita_min:
                    escalaoDoAluno = escalao.escalao
                    percParaAplicarCapital = escalao.comparticipacao_da_familia
                    break
                elif percParaEscaloes >= escalao.perc_rend_per_capita_min and percParaEscaloes < escalao.perc_rend_per_capita_max:
                    escalaoDoAluno = escalao.escalao
                    percParaAplicarCapital = escalao.comparticipacao_da_familia
                    break
            valorFinal = RMM * (percParaAplicarCapital/100)


            # Vereficar se exista ja o registo
            if MensalidadeAluno.objects.filter(Q(ano=now.year) & Q(mes=now.month) & Q(aluno_id=financa.aluno_id)).exists():
                mensalidade = MensalidadeAluno.objects.get(Q(ano=now.year) & Q(mes=now.month) & Q(aluno_id=financa.aluno_id))
                mensalidade.aluno_id = financa.aluno_id
                mensalidade.mes = now.month
                mensalidade.ano = now.year
                mensalidade.mensalidade_calc = Decimal(f"{valorFinal:.2f}")
                mensalidade.escalao = escalaoDoAluno
                mensalidade.save()
            else:
                mensalidade = MensalidadeAluno()
                mensalidade.aluno_id = financa.aluno_id
                mensalidade.mes = now.month
                mensalidade.ano = now.year
                mensalidade.mensalidade_calc = Decimal(f"{valorFinal:.2f}")
                mensalidade.escalao = escalaoDoAluno
                mensalidade.save()




        # Calcula as comparticoes da SS
        for mensalidade in MensalidadeAluno.objects.all():

            if ComparticaoMensalSS.objects.filter(aluno_mensalidade_id=mensalidade.ma_id).exists():
                comparticao = ComparticaoMensalSS.objects.get(aluno_mensalidade_id=mensalidade.ma_id)
                comparticao.ano_letivo = now.date()
                comparticao.periodo_inicio = now.date()

                if(comparticao.aluno_id.comparticao_ss_custom is None):
                    comparticao.mensalidade_valor = mensalidade.aluno_id.programa_id.custo
                else:
                    comparticao.mensalidade_valor = comparticao.aluno_id.comparticao_ss_custom

                comparticao.programa_ss = mensalidade.aluno_id.programa_id.nome
                comparticao.aluno_id = mensalidade.aluno_id
                comparticao.aluno_mensalidade_id = mensalidade
                comparticao.save()
            else:
                comparticao = ComparticaoMensalSS()
                comparticao.ano_letivo = now.date()
                comparticao.periodo_inicio = now.date()

                if(comparticao.aluno_id.comparticao_ss_custom is None):
                    comparticao.mensalidade_valor = mensalidade.aluno_id.programa_id.custo
                else:
                    comparticao.mensalidade_valor = comparticao.aluno_id.comparticao_ss_custom

                comparticao.programa_ss = mensalidade.aluno_id.programa_id.nome
                comparticao.aluno_id = mensalidade.aluno_id
                comparticao.aluno_mensalidade_id = mensalidade
                comparticao.save()

        return redirect("show_aluno_financas")

    # Filtros
    filtros = {"nome": request.GET.get('nome', ''), "sala": request.GET.get('sala', ''), "mes": int(request.GET.get('mes')) if request.GET.get('mes') else '', "ano": int(request.GET.get('ano')) if request.GET.get('ano') else ''}

    # Valores para escolher os filtros no template
    valoresDosFiltros = {"salas": Sala.objects.all(), "meses_range": range(1, 13), "anos_range": range(2000, dt.now().year + 1)}




    # Vai buscar dados
    financas = AlunoFinancas.objects.all()
    mensalidades = MensalidadeAluno.objects.select_related("comparticao").order_by('-ano','mes')
    comparticoesSS = ComparticaoMensalSS.objects.all()




    # Aplica os filtros
    if filtros["nome"]:
        mensalidades = mensalidades.filter(aluno_id__nome_proprio__icontains=filtros["nome"])

    if filtros["sala"]:
        mensalidades = mensalidades.filter(aluno_id__sala_id__sala_nome__icontains=filtros["sala"])

    if filtros["mes"]:
        mensalidades = mensalidades.filter(mes=filtros["mes"])

    if filtros["ano"]:
        mensalidades = mensalidades.filter(ano=filtros["ano"])

    context = {
        "financas": financas,
        "mensalidades": mensalidades,
        "comparticoesSS": comparticoesSS,
        "valoresDosFiltros": valoresDosFiltros,
        "filtros": filtros
    }

    return render(request, "show_aluno_financas.html", context)




def show_contactos(request):
    # URL query parameters
    query = request.GET.get("q", "")




    # Get guardians
    encarregadosEducacao = ResponsavelEducativo.objects.prefetch_related("alunos")
    # Apply search filter
    if query:
        encarregadosEducacao = encarregadosEducacao.filter(Q(nome_proprio__icontains=query) | Q(apelido__icontains=query))




    # Render the template with context
    context = {"guardians": encarregadosEducacao, "salas": Sala.objects.all(), "guardiansCount": encarregadosEducacao.count(), "filtersValue": {"name": query}}
    return render(request, "show_contactos.html", context)




def show_contactos_details(request, responsavel_id):
    guardian = ResponsavelEducativo.objects.prefetch_related("alunos").get(responsavel_educativo_id=responsavel_id)

    context = {"guardian": guardian}
    return render(request, "show_contactos_details.html", context)




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
    aluno = Aluno.objects.select_related("sala_id").prefetch_related("responsaveis_educativos_ids").get(aluno_id=aluno_id)

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