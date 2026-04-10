
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
                mensalidade.mensalidade_paga = 0
                mensalidade.escalao = escalaoDoAluno
                mensalidade.save()








        # Calcula as comparticoes da SS
        for mensalidade in MensalidadeAluno.objects.all():

            if ComparticaoMensalSS.objects.filter(aluno_mensalidade_id=mensalidade.ma_id).exists():
                comparticao = ComparticaoMensalSS.objects.get(aluno_mensalidade_id=mensalidade.ma_id)
                comparticao.ano_letivo = now.date()
                comparticao.periodo_inicio_mes = mensalidade.mes
                comparticao.periodo_inicio_ano = mensalidade.ano
                comparticao.aluno_id = mensalidade.aluno_id

                if(comparticao.aluno_id.comparticao_ss_custom is None):
                    comparticao.mensalidade_valor = mensalidade.aluno_id.programa_id.custo
                else:
                    comparticao.mensalidade_valor = comparticao.aluno_id.comparticao_ss_custom

                comparticao.programa_ss = mensalidade.aluno_id.programa_id.nome
                comparticao.aluno_mensalidade_id = mensalidade
                comparticao.save()
            else:
                comparticao = ComparticaoMensalSS()
                comparticao.ano_letivo = now.date()
                comparticao.periodo_inicio_mes = mensalidade.mes
                comparticao.periodo_inicio_ano = mensalidade.ano
                comparticao.aluno_id = mensalidade.aluno_id

                if(comparticao.aluno_id.comparticao_ss_custom is None):
                    comparticao.mensalidade_valor = mensalidade.aluno_id.programa_id.custo
                else:
                    comparticao.mensalidade_valor = comparticao.aluno_id.comparticao_ss_custom

                comparticao.mensalidade_paga = 0.0
                comparticao.programa_ss = mensalidade.aluno_id.programa_id.nome
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




    # Aplica os filtros para as mensalidades e para as comparticoes da SS
    if filtros["nome"]:
        mensalidades = mensalidades.filter(Q(aluno_id__nome_proprio__icontains=filtros["nome"]) | Q(aluno_id__apelido__icontains=filtros["nome"]))
        comparticoesSS = comparticoesSS.filter(Q(aluno_id__nome_proprio__icontains=filtros["nome"]) | Q(aluno_id__apelido__icontains=filtros["nome"]))

    if filtros["sala"]:
        mensalidades = mensalidades.filter(aluno_id__sala_id__sala_nome__icontains=filtros["sala"])
        comparticoesSS = comparticoesSS.filter(aluno_id__sala_id__sala_nome__icontains=filtros["sala"])

    if filtros["mes"]:
        mensalidades = mensalidades.filter(mes=filtros["mes"])
        comparticoesSS = comparticoesSS.filter(periodo_inicio__month=filtros["mes"])

    if filtros["ano"]:
        mensalidades = mensalidades.filter(ano=filtros["ano"])
        comparticoesSS = comparticoesSS.filter(periodo_inicio__year=filtros["ano"])




    # Calcula as dividas de cada aluno
    dividasPorAlunoID = {}
    for aluno in Aluno.objects.all():
        mensalidadesDoAluno = MensalidadeAluno.objects.filter(aluno_id=aluno.aluno_id)
        divida = 0
        for mensalidadeDoAluno in mensalidadesDoAluno:
            divida += mensalidadeDoAluno.mensalidade_calc - mensalidadeDoAluno.mensalidade_paga
        dividasPorAlunoID[aluno.aluno_id] = divida





    context = {
        "financas": financas,
        "mensalidades": mensalidades,
        "dividas": dividasPorAlunoID,
        "comparticoesSS": comparticoesSS,
        "valoresDosFiltros": valoresDosFiltros,
        "filtros": filtros
    }

    return render(request, "show_aluno_financas.html", context)




def insert_financas(request):
    if request.method == "POST":
        form = FinancasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_aluno_financas')
        else:
            print(form.errors)
    else:
        form = FinancasForm()
        return render(request, 'insert_financas.html', {'form': form})




def edit_financas(request, financa_id):
    alunoFinanca = get_object_or_404(AlunoFinancas, pk=financa_id)
    if request.method == "POST":
        form = FinancasForm(request.POST, instance=alunoFinanca)
        if form.is_valid():
            form.save()
            return redirect('show_aluno_financas')
        else:
            print(form.errors)
    else:
        form = FinancasForm(instance=alunoFinanca)
        return render(request, 'insert_financas.html', {'form': form})




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
    query_valencia = request.GET.get("valencia", "")
    query_room = request.GET.get("room", "")

    # Buscar salas
    salas = Sala.objects.all().order_by('sala_valencia', 'sala_nome')

    # Aplicar filtros
    if query_valencia:
        salas = salas.filter(sala_valencia__icontains=query_valencia)
    if query_room:
        salas = salas.filter(sala_nome__icontains=query_room)

    # Obter os valores para os filtros no template
    valoresFiltros = {"valencias": Sala.objects.values_list("sala_valencia", flat=True).distinct(), "salas_nomes": Sala.objects.values_list("sala_nome", flat=True).distinct()}

    context = {
        "salas": salas,
        "valoresFiltros": valoresFiltros,
    }
    return render(request, "show_sala.html", context)




def insert_sala_view(request):
    if request.method == "POST":
        form = SalaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_salas')
        else:
            print(form.errors)
    else:
        form = SalaForm()
        return render(request, 'insert_sala.html', {'form': form})




def edit_sala(request, sala_id):
    sala = get_object_or_404(Sala, pk=sala_id)
    if request.method == "POST":
        form = SalaForm(request.POST, instance=sala)
        if form.is_valid():
            form.save()
            return redirect('show_salas')
    else:
        form = SalaForm(instance=sala)
    return render(request, 'edit_sala.html', {'form': form})




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