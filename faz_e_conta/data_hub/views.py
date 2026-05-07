from _datetime import datetime as dt, timezone
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .auto_gen_id_views import *
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import date



#Pagina inicial
def starter_page(request):

    nome_do_utilizador = ""
    if request.user.is_authenticated:
        nome_do_utilizador = request.user.username
    else:
        nome_do_utilizador = ""


    context = {"username": nome_do_utilizador}
    return render(request, "starter_page.html", context)








# Estudantes
@login_required
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

def show_student_details(request, aluno_id):
    aluno = Aluno.objects.select_related("sala_id").prefetch_related("responsaveis_educativos_ids").get(aluno_id=aluno_id)

    context = {"aluno": aluno}
    return render(request, "show_student_details.html", context)

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








# Resposaveis educativos
@login_required
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








# Salas
@login_required
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








# Despesas
@login_required
def show_despesas(request):
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")


    despesasVar = DespesasVariavel.objects.all()
    despesasFix = DespesaFixa.objects.all()

    if start_date and end_date:
        despesasFix = despesasFix.filter(data__range=[start_date, end_date])
        despesasVar = despesasVar.filter(data__range=[start_date, end_date])

    total_fixas = despesasFix.aggregate(Sum('valor'))['valor__sum'] or 0.0
    total_variaveis = despesasVar.aggregate(Sum('valor'))['valor__sum'] or 0.0
    total_geral = total_fixas + total_variaveis

    valoresFiltros = {
        "start_date": start_date,
        "end_date": end_date,
    }

    totais = {
        "fixas": total_fixas,
        "variaveis": total_variaveis,
        "geral": total_geral,
    }

    despesas = {
        "despesasFix": despesasFix,
        "despesasVar": despesasVar,
    }

    context = {
        "despesas": despesas,
        "valoresFiltros": valoresFiltros,
        "totais": totais,
    }
    return render(request, "show_despesa.html", context)

def insert_despesa_view(request, tipo_despesa):
    if tipo_despesa == 'fixa':
        form_class = DespesaFixaForm
        titulo = "Inserir Despesa Fixa"
    else:
        form_class = DespesasVariavelForm
        titulo = "Inserir Despesa Variável"

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_despesas')
    else:
        form = form_class()

    return render(request, 'insert_despesa.html', {'form': form, 'titulo': titulo})

def edit_despesasFixas(request, despesaFixa_id):
    despesaFixa = get_object_or_404(DespesaFixa, pk=despesaFixa_id)
    if request.method == "POST":
        form = DespesaFixaForm(request.POST, instance=despesaFixa)
        if form.is_valid():
            form.save()
            return redirect('show_despesas')
        else:
            print(form.errors)
    else:
        form = DespesaFixaForm(instance=despesaFixa)
        return render(request, 'insert_despesa.html', {'form': form})

def edit_despesasVariaveis(request, despesaVariavel_id):
    despesaVariavel = get_object_or_404(DespesasVariavel, pk=despesaVariavel_id)
    if request.method == "POST":
        form = DespesasVariavelForm(request.POST, instance=despesaVariavel)
        if form.is_valid():
            form.save()
            return redirect('show_despesas')
        else:
            print(form.errors)
    else:
        form = DespesasVariavelForm(instance=despesaVariavel)
        return render(request, 'insert_despesa.html', {'form': form})








# Financas
@login_required
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
        comparticoesSS = comparticoesSS.filter(periodo_inicio_mes=filtros["mes"])

    if filtros["ano"]:
        mensalidades = mensalidades.filter(ano=filtros["ano"])
        comparticoesSS = comparticoesSS.filter(periodo_inicio_ano=filtros["ano"])




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








# Saude financeira
@login_required
def show_saude_fianceira(request):
    # Valores para os filtros na pagina
    anos = range(2000, timezone.now().year+1)
    meses = range(1, 13)
    dias = range(1, 32)
    valoresFiltros = {
        "anos": anos,
        "meses": meses,
        "dias": dias
    }




    # Post
    valoresSelecionadosPostFiltros = {
        "dia": None,
        "mes": None,
        "ano": None
    }
    if request.method == "POST":
        # Pegar os filtros
        dia = request.POST.get("dia")
        mes = request.POST.get("mes")
        ano = request.POST.get("ano")

        if dia == "":
            dia = None
        if mes == "":
            mes = None
        if ano == "":
            ano = None

        if dia is not None:
            valoresSelecionadosPostFiltros["dia"] = int(dia)
        else:
            dia = timezone.now().day
            valoresSelecionadosPostFiltros["dia"] = dia
        if mes is not None:
            valoresSelecionadosPostFiltros["mes"] = int(mes)
        else:
            mes = timezone.now().month
            valoresSelecionadosPostFiltros["mes"] = mes
        if ano is not None:
            valoresSelecionadosPostFiltros["ano"] = int(ano)
        else:
            ano = timezone.now().year
            valoresSelecionadosPostFiltros["ano"] = ano




        # Data do calculo
        data = date(int(ano), int(mes), int(dia))




        # Calcular o total custo das despesas
        despesas_fixas = DespesaFixa.objects.all()
        despesas_variaveis = DespesasVariavel.objects.filter(
            data__year=int(ano),
            data__month=int(mes),
            data__day__lte=int(dia)
        )

        custo_total_despesas_fixas = 0
        custo_total_despesas_variaveis = 0
        custo_total_despesas = 0
        for d in despesas_fixas:
            custo_total_despesas_fixas += d.valor
        for d in despesas_variaveis:
            custo_total_despesas_variaveis += d.valor
        custo_total_despesas = custo_total_despesas_fixas + custo_total_despesas_variaveis

        print(f"Custo das variaveis: {custo_total_despesas_variaveis}")
        print("Datas:")
        print(DespesasVariavel.objects.all().values('data')[:5])




        # Calcular o total custo das mensalidades
        mensalidades = MensalidadeAluno.objects.filter(ano = ano, mes = mes)
        valor_total_mensalidades_pagas = 0
        valor_total_mensalidades_nao_pagas = 0
        valor_total_mensalidades = 0
        for m in mensalidades:
            valor_total_mensalidades_pagas += m.mensalidade_paga
            valor_total_mensalidades += m.mensalidade_calc
        valor_total_mensalidades_nao_pagas = valor_total_mensalidades - valor_total_mensalidades_pagas




        # Calcular o total custo das comparticoes
        comparticoes = ComparticaoMensalSS.objects.filter(periodo_inicio_ano=ano, periodo_inicio_mes=mes)
        valor_total_comparticoes_pagas = 0
        valor_total_comparticoes_nao_pagas = 0
        valor_total_comparticoes = 0
        for c in comparticoes:
            valor_total_comparticoes_pagas += c.mensalidade_paga
            valor_total_comparticoes += c.mensalidade_valor
        valor_total_comparticoes_nao_pagas = valor_total_comparticoes - valor_total_comparticoes_pagas




        # Criar um registo de saude financeira
        SaudeFinanceira.objects.create(
            custo_despesas_totais = custo_total_despesas,
            mensalidades_pagas_total = valor_total_mensalidades_pagas,
            mensalidades_nao_pagas_total = valor_total_mensalidades_nao_pagas,
            comparticoes_pagas_total = valor_total_comparticoes_pagas,
            comparticoes_nao_pagas_total = valor_total_comparticoes_nao_pagas,
            data = data,
            receita = (valor_total_mensalidades_pagas + valor_total_comparticoes_pagas) - custo_total_despesas
        ).save()




    # Get
    dia = request.GET.get("dia")
    mes = request.GET.get("mes")
    ano = request.GET.get("ano")
    valoresSelecionadosGetFiltros = {
        "dia": None,
        "mes": None,
        "ano": None
    }
    if dia == "":
        dia = None
    if mes == "":
        mes = None
    if ano == "":
        ano = None


    saudes_financeiras = SaudeFinanceira.objects.all()
    if dia is not None:
        saudes_financeiras = saudes_financeiras.filter(data__day = dia)
        valoresSelecionadosGetFiltros["dia"] = int(dia)
    if mes is not None:
        saudes_financeiras = saudes_financeiras.filter(data__month = mes)
        valoresSelecionadosGetFiltros["mes"] = int(mes)
    if ano is not None:
        saudes_financeiras = saudes_financeiras.filter(data__year = ano)
        valoresSelecionadosGetFiltros["ano"] = int(ano)


    contexto = {
        "saudesFinanceiras": saudes_financeiras,
        "valoresFiltros": valoresFiltros,
        "valoresSelecionadosGetFiltros": valoresSelecionadosGetFiltros,
        "valoresSelecionadosPostFiltros": valoresSelecionadosPostFiltros
    }

    return render(request, 'show_saude_financeira.html', contexto)








# Autentificacao
def insert_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_active = False
            user.save()

            return redirect('show_despesas')
    else:
        form = UserForm()
        return render(request, 'insert_user.html', {'form': form})