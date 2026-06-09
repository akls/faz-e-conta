from _datetime import datetime as dt, timezone
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
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
    alumni = request.GET.get("alumni", "")



    # Get alunos in the data base
    alunos = Aluno.objects.all()
    # Apply filters
    if query:
        alunos = alunos.filter(Q(nome_proprio__icontains=query) | Q(apelido__icontains=query))
    if sala_filter:
        alunos = alunos.filter(Q(sala_id__sala_valencia__icontains=sala_filter) | Q(sala_id__sala_nome__icontains=sala_filter))
    if alumni:
        alumni = True
        alunos = alunos.filter(archive_flag=alumni)
    else:
        alunos = alunos.filter(archive_flag=False)




    # Render the template with context
    alunoFields = ["aluno_id", "nome_proprio", "apelido", "processo", "numero_documento", "data_admissao", "sala_id__sala_valencia", "sala_id__sala_nome"]
    context = {"alunos": alunos.values(*alunoFields), "salas": Sala.objects.all(), "alunoCount": alunos.count(), "filtersValue": {"sala": sala_filter, "name": query, "alumni": alumni}}
    return render(request, "show_students.html", context)

def show_student_details(request, aluno_id):
    aluno = Aluno.objects.select_related("sala_id").prefetch_related("responsaveis_educativos_ids").get(aluno_id=aluno_id)

    context = {"aluno": aluno}
    return render(request, "show_student_details.html", context)

def insert_aluno_view(request):
    if request.method == "POST":
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_students')
        else:
            print(form.errors)
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
            escaloes = EscaloesRendimento.objects.all().order_by("perc_rend_per_capita_min")
            escalaoDoAluno = ""
            percParaAplicarCapital = 0.0
            for escalao in escaloes:
                minimo = float(escalao.perc_rend_per_capita_min)

                maximo = escalao.perc_rend_per_capita_max
                if maximo is None or maximo == "":
                    maximo = None
                else:
                    maximo = float(maximo)

                if maximo is None and percParaEscaloes >= minimo:
                    escalaoDoAluno = escalao.escalao
                    percParaAplicarCapital = escalao.comparticipacao_da_familia
                    break
                elif maximo is not None and minimo <= percParaEscaloes < maximo:
                    escalaoDoAluno = escalao.escalao
                    percParaAplicarCapital = escalao.comparticipacao_da_familia
                    break
            valorFinal = RMM * (percParaAplicarCapital/100)


            # Vereficar se exista ja o registo
            if MensalidadeAluno.objects.filter(Q(data_inicio__year=now.year) & Q(data_inicio__month=now.month) & Q(aluno_id=financa.aluno_id)).exists():
                mensalidade = MensalidadeAluno.objects.get(Q(data_inicio__year=now.year) & Q(data_inicio__month=now.month) & Q(aluno_id=financa.aluno_id))
                mensalidade.aluno_id = financa.aluno_id
                mensalidade.mensalidade_calc = Decimal(f"{valorFinal:.2f}")
                mensalidade.escalao = escalaoDoAluno
                mensalidade.save()
            else:
                mensalidade = MensalidadeAluno()
                mensalidade.aluno_id = financa.aluno_id
                mensalidade.mensalidade_calc = Decimal(f"{valorFinal:.2f}")
                mensalidade.mensalidade_paga = 0
                mensalidade.escalao = escalaoDoAluno
                mensalidade.save()








        # Calcula as comparticoes da SS
        for mensalidade in MensalidadeAluno.objects.all():

            if ComparticaoMensalSS.objects.filter(aluno_mensalidade_id=mensalidade.ma_id).exists():
                comparticao = ComparticaoMensalSS.objects.get(aluno_mensalidade_id=mensalidade.ma_id)
                comparticao.ano_letivo = now.date()
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
    mensalidades = MensalidadeAluno.objects.all()
    comparticoesSS = ComparticaoMensalSS.objects.all()




    # Aplica os filtros para as mensalidades e para as comparticoes da SS
    if filtros["nome"]:
        mensalidades = mensalidades.filter(Q(aluno_id__nome_proprio__icontains=filtros["nome"]) | Q(aluno_id__apelido__icontains=filtros["nome"]))
        comparticoesSS = comparticoesSS.filter(Q(aluno_id__nome_proprio__icontains=filtros["nome"]) | Q(aluno_id__apelido__icontains=filtros["nome"]))

    if filtros["sala"]:
        mensalidades = mensalidades.filter(aluno_id__sala_id__sala_nome__icontains=filtros["sala"])
        comparticoesSS = comparticoesSS.filter(aluno_id__sala_id__sala_nome__icontains=filtros["sala"])

    if filtros["mes"]:
        mensalidades = mensalidades.filter(data_inicio__month=filtros["mes"])
        comparticoesSS = comparticoesSS.filter(data_inicio__month=filtros["mes"])

    if filtros["ano"]:
        mensalidades = mensalidades.filter(data_inicio__year=filtros["ano"])
        comparticoesSS = comparticoesSS.filter(data_inicio__year=filtros["ano"])




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
            aluno = form.cleaned_data["aluno_id"]

            if AlunoFinancas.objects.filter(aluno_id=aluno).exists():
                form.add_error("aluno_id", "Este aluno já tem finanças registadas.")
            else:
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

def insert_pagamentos(request):

    mensagem = ""
    item = {}
    valoresDosFiltros = {}

    if request.method == "POST":

        if not all([request.POST.get("pagamentoOpcao"), request.POST.get("aluno"), request.POST.get("valorPagamento"), request.POST.get("mes"), request.POST.get("ano"), request.POST.get("metodoPagamento"), request.POST.get("dataPagamento")]):
            mensagem = "Erro: Preencha todos os campos"

        else:
            opcao = request.POST.get("pagamentoOpcao")
            alunoId = request.POST.get("aluno")
            mes = int(request.POST.get("mes"))
            ano = int(request.POST.get("ano"))
            valorPagamento = float(request.POST.get("valorPagamento"))
            metodoPagamento = MetodoPagamento.objects.filter(pk=request.POST.get("metodoPagamento")).first()
            dataPagamento = request.POST.get("dataPagamento")

            valoresDosFiltros = {
                "aluno": int(request.POST.get("aluno")),
                "pagamentoOpcao": request.POST.get("pagamentoOpcao"),
                "mes": int(request.POST.get("mes")),
                "ano": int(request.POST.get("ano")),
                "valorPagamento": request.POST.get("valorPagamento"),
                "metodoPagamento": int(request.POST.get("metodoPagamento")),
                "dataPagamento": request.POST.get("dataPagamento"),
            }

            if valorPagamento <= 0:
                mensagem = "Erro: O valor do pagamento deve ser positivo e maior que 0"

            elif opcao == "mensalidade":
                mensalidade = MensalidadeAluno.objects.filter(
                    aluno_id=alunoId,
                    data_inicio__month=mes,
                    data_inicio__year=ano
                ).first()

                if mensalidade is None:
                    mensagem = "Erro: Mensalidade não encontrada"
                else:
                    PagamentoMensalidade.objects.create(
                        mensalidade_id=mensalidade,
                        metodo_pagamento_id=metodoPagamento,
                        valor=valorPagamento,
                        data=dataPagamento
                    )
                    mensalidade.mensalidade_paga = mensalidade.pagamentos.aggregate(Sum("valor"))["valor__sum"] or 0
                    mensalidade.data_fim = dataPagamento
                    mensalidade.save()

                    if mensalidade.mensalidade_paga > mensalidade.mensalidade_calc:
                        mensagem = "Aviso: O valor pago ultrapassa o valor da mensalidade"
                    else:
                        mensagem = "Pagamento registado"

                    item["nome"] = f"{mensalidade.aluno_id.nome_proprio} {mensalidade.aluno_id.apelido}"
                    item["tipo"] = "Mensalidade"
                    item["valorAPagar"] = mensalidade.mensalidade_calc
                    item["valorPago"] = mensalidade.mensalidade_paga

            elif opcao == "comparticao":
                comparticao = ComparticaoMensalSS.objects.filter(
                    aluno_id=alunoId,
                    data_inicio__month=mes,
                    data_inicio__year=ano
                ).first()

                if comparticao is None:
                    mensagem = "Erro: Comparticão não encontrada"
                else:
                    PagamentoComparticao.objects.create(
                        comparticao_id=comparticao,
                        metodo_pagamento_id=metodoPagamento,
                        valor=valorPagamento,
                        data=dataPagamento
                    )
                    comparticao.mensalidade_paga = comparticao.pagamentos.aggregate(Sum("valor"))["valor__sum"] or 0
                    comparticao.data_fim = dataPagamento
                    comparticao.save()

                    if comparticao.mensalidade_paga > comparticao.mensalidade_valor:
                        mensagem = "Aviso: O valor pago ultrapassa o valor da comparticão"
                    else:
                        mensagem = "Pagamento registado"

                    item["nome"] = f"{comparticao.aluno_id.nome_proprio} {comparticao.aluno_id.apelido}"
                    item["tipo"] = "Comparticação"
                    item["valorAPagar"] = comparticao.mensalidade_valor
                    item["valorPago"] = comparticao.mensalidade_paga

    alunos = Aluno.objects.filter(archive_flag=False).distinct()
    meses = range(1, 13)
    anos = range(2000, date.today().year + 1)
    metodosPagamento = MetodoPagamento.objects.all()

    contexto = {
        "alunos": alunos,
        "meses": meses,
        "metodosPagamento": metodosPagamento,
        "anos": anos,
        "mensagem": mensagem,
        "item": item,
        "valoresDosFiltros": valoresDosFiltros
    }
    return render(request, 'insert_pagamentos.html', contexto)

def show_pagamentos_mensalidade(request, mensalidade_id):
    mensalidade = get_object_or_404(MensalidadeAluno, pk=mensalidade_id)

    contexto = {
        "titulo": "Pagamentos da Mensalidade",
        "aluno": mensalidade.aluno_id,
        "data": mensalidade.data_inicio,
        "valorAPagar": mensalidade.mensalidade_calc,
        "valorPago": mensalidade.mensalidade_paga,
        "pagamentos": mensalidade.pagamentos.all(),
        "editarUrl": "edit_pagamento_mensalidade"
    }
    return render(request, 'show_pagamentos.html', contexto)

def show_pagamentos_comparticao(request, comparticao_id):
    comparticao = get_object_or_404(ComparticaoMensalSS, pk=comparticao_id)

    contexto = {
        "titulo": "Pagamentos da Comparticipação",
        "aluno": comparticao.aluno_id,
        "data": comparticao.data_inicio,
        "valorAPagar": comparticao.mensalidade_valor,
        "valorPago": comparticao.mensalidade_paga,
        "pagamentos": comparticao.pagamentos.all(),
        "editarUrl": "edit_pagamento_comparticao"
    }
    return render(request, 'show_pagamentos.html', contexto)

def edit_pagamento_mensalidade(request, pagamento_id):
    pagamento = get_object_or_404(PagamentoMensalidade, pk=pagamento_id)
    mensalidade = pagamento.mensalidade_id

    if request.method == "POST":
        form = PagamentoMensalidadeForm(request.POST, instance=pagamento)
        if form.is_valid():
            form.save()
            mensalidade.mensalidade_paga = mensalidade.pagamentos.aggregate(Sum("valor"))["valor__sum"] or 0
            mensalidade.save()
            return redirect('show_pagamentos_mensalidade', mensalidade_id=mensalidade.ma_id)
        else:
            print(form.errors)
    else:
        form = PagamentoMensalidadeForm(instance=pagamento)

    contexto = {
        "form": form,
        "voltarUrl": reverse('show_pagamentos_mensalidade', kwargs={"mensalidade_id": mensalidade.ma_id})
    }
    return render(request, 'edit_pagamento.html', contexto)

def edit_pagamento_comparticao(request, pagamento_id):
    pagamento = get_object_or_404(PagamentoComparticao, pk=pagamento_id)
    comparticao = pagamento.comparticao_id

    if request.method == "POST":
        form = PagamentoComparticaoForm(request.POST, instance=pagamento)
        if form.is_valid():
            form.save()
            comparticao.mensalidade_paga = comparticao.pagamentos.aggregate(Sum("valor"))["valor__sum"] or 0
            comparticao.save()
            return redirect('show_pagamentos_comparticao', comparticao_id=comparticao.mss_id)
        else:
            print(form.errors)
    else:
        form = PagamentoComparticaoForm(instance=pagamento)

    contexto = {
        "form": form,
        "voltarUrl": reverse('show_pagamentos_comparticao', kwargs={"comparticao_id": comparticao.mss_id})
    }
    return render(request, 'edit_pagamento.html', contexto)

def insert_metodo_pagamento_view(request):
    if request.method == "POST":
        form = MetodoPagamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('insert_pagamentos')
        else:
            print(form.errors)
    else:
        form = MetodoPagamentoForm()
    return render(request, 'insert_metodo_pagamento.html', {'form': form})







# Funçoes dos calculos da saude financeira
def calcularCustoPorCrianca(data_inicio, data_fim):
    despesas_fixas = DespesaFixa.objects.all()
    despesas_variaveis = DespesasVariavel.objects.filter(data__range=(data_inicio, data_fim))
    custo_total_despesas = sum(d.valor for d in despesas_fixas) + sum(d.valor for d in despesas_variaveis)

    num_criancas = Aluno.objects.filter(archive_flag=False).count()

    if num_criancas == 0:
        return 0

    return custo_total_despesas / num_criancas

def balancoGlobal(request):

    valoresSelecionadosPostFiltros = {}

    data_inicio = request.POST.get("data_inicio")
    data_fim = request.POST.get("data_fim")

    # Se não preenchido, usa o mês atual
    if not data_inicio:
        data_inicio = date(timezone.now().year, timezone.now().month, 1)
    else:
        data_inicio = date.fromisoformat(data_inicio)

    if not data_fim:
        data_fim = timezone.now().date()
    else:
        data_fim = date.fromisoformat(data_fim)

    valoresSelecionadosPostFiltros["data_inicio"] = data_inicio
    valoresSelecionadosPostFiltros["data_fim"] = data_fim

    # Calcular despesas
    despesas_fixas = DespesaFixa.objects.all()
    despesas_variaveis = DespesasVariavel.objects.filter(
        data__range=(data_inicio, data_fim)
    )

    custo_total_despesas = sum(d.valor for d in despesas_fixas) + sum(d.valor for d in despesas_variaveis)

    # Calcular mensalidades
    mensalidades = MensalidadeAluno.objects.filter(
        data_inicio__range=(data_inicio, data_fim)
    )
    valor_total_mensalidades_pagas = sum(m.mensalidade_paga for m in mensalidades)
    valor_total_mensalidades = sum(m.mensalidade_calc for m in mensalidades)
    valor_total_mensalidades_nao_pagas = valor_total_mensalidades - valor_total_mensalidades_pagas

    # Calcular comparticipações
    comparticoes = ComparticaoMensalSS.objects.filter(
        data_inicio__range=(data_inicio, data_fim)
    )
    valor_total_comparticoes_pagas = sum(c.mensalidade_paga for c in comparticoes)
    valor_total_comparticoes = sum(c.mensalidade_valor for c in comparticoes)
    valor_total_comparticoes_nao_pagas = valor_total_comparticoes - valor_total_comparticoes_pagas

    # Gravar
    SaudeFinanceiraBalancoGlobal.objects.create(
        custo_despesas_totais=custo_total_despesas,
        mensalidades_pagas_total=valor_total_mensalidades_pagas,
        mensalidades_nao_pagas_total=valor_total_mensalidades_nao_pagas,
        comparticoes_pagas_total=valor_total_comparticoes_pagas,
        comparticoes_nao_pagas_total=valor_total_comparticoes_nao_pagas,
        data_inicio = data_inicio,
        data_fim = data_fim,
        receita=(valor_total_mensalidades_pagas + valor_total_comparticoes_pagas) - custo_total_despesas
    )
    return valoresSelecionadosPostFiltros

def balancoValencia(request):
    data_inicio = request.POST.get("data_inicio")
    data_fim = request.POST.get("data_fim")
    valencia = request.POST.get("valencia")

    if not data_inicio:
        data_inicio = date(timezone.now().year, timezone.now().month, 1)
    else:
        data_inicio = date.fromisoformat(data_inicio)

    if not data_fim:
        data_fim = timezone.now().date()
    else:
        data_fim = date.fromisoformat(data_fim)

    custo_por_crianca = calcularCustoPorCrianca(data_inicio, data_fim)

    # Alunos nesta valência
    alunos = Aluno.objects.filter(sala_id__sala_valencia=valencia, archive_flag=False)
    num_alunos = alunos.count()

    if num_alunos == 0:
        return

    # Mensalidades dos alunos desta valência no período
    mensalidades = MensalidadeAluno.objects.filter(
        aluno_id__in=alunos,
        data_inicio__range=(data_inicio, data_fim)
    )
    mensalidades_pagas = sum(m.mensalidade_paga for m in mensalidades)

    # Comparticipações dos alunos desta valência no período
    comparticoes = ComparticaoMensalSS.objects.filter(
        aluno_id__in=alunos,
        data_inicio__range=(data_inicio, data_fim)
    )
    comparticoes_pagas = sum(c.mensalidade_paga for c in comparticoes)

    # Balanço por valência
    balanco = (mensalidades_pagas + comparticoes_pagas) / num_alunos - custo_por_crianca

    SaudeFinanceiraBalancoValencia.objects.create(
        valencia=valencia,
        mensalidades_pagas_total=mensalidades_pagas,
        comparticoes_pagas_total=comparticoes_pagas,
        num_alunos=num_alunos,
        custo_por_crianca=custo_por_crianca,
        balanco=balanco,
        data_inicio=data_inicio,
        data_fim=data_fim
    )

def balancoEscalao(request):
    data_inicio = request.POST.get("data_inicio")
    data_fim = request.POST.get("data_fim")
    escalao = request.POST.get("escalao")

    if not data_inicio:
        data_inicio = date(timezone.now().year, timezone.now().month, 1)
    else:
        data_inicio = date.fromisoformat(data_inicio)

    if not data_fim:
        data_fim = timezone.now().date()
    else:
        data_fim = date.fromisoformat(data_fim)

    custo_por_crianca = calcularCustoPorCrianca(data_inicio, data_fim)

    # Mensalidades com este escalão no período
    mensalidades = MensalidadeAluno.objects.filter(
        escalao=escalao,
        data_inicio__date__range=(data_inicio, data_fim)
    )
    mensalidades_pagas = sum(m.mensalidade_paga for m in mensalidades)


    num_alunos = mensalidades.values('aluno_id').distinct().count()
    if num_alunos == 0:
        return


    # Comparticipações dos alunos neste escalão no período
    comparticoes = ComparticaoMensalSS.objects.filter(
        aluno_id__in=mensalidades.values('aluno_id'),
        data_inicio__date__range=(data_inicio, data_fim)
    )
    comparticoes_pagas = sum(c.mensalidade_paga for c in comparticoes)
    balanco = (mensalidades_pagas + comparticoes_pagas) / num_alunos - custo_por_crianca

    SaudeFinanceiraBalancoEscalao.objects.create(
        escalao=escalao,
        mensalidades_pagas_total=mensalidades_pagas,
        comparticoes_pagas_total=comparticoes_pagas,
        num_alunos=num_alunos,
        custo_por_crianca=custo_por_crianca,
        balanco=balanco,
        data_inicio=data_inicio,
        data_fim=data_fim
    )

def balancoAluno(request):
    data_inicio = request.POST.get("data_inicio")
    data_fim = request.POST.get("data_fim")
    aluno_id = request.POST.get("aluno")

    if not data_inicio:
        data_inicio = date(timezone.now().year, timezone.now().month, 1)
    else:
        data_inicio = date.fromisoformat(data_inicio)

    if not data_fim:
        data_fim = timezone.now().date()
    else:
        data_fim = date.fromisoformat(data_fim)

    # Precisa de um aluno selecionado
    aluno = Aluno.objects.filter(pk=aluno_id).first()
    if aluno is None:
        return

    custo_por_crianca = calcularCustoPorCrianca(data_inicio, data_fim)

    # Mensalidades deste aluno no periodo
    mensalidades = MensalidadeAluno.objects.filter(
        aluno_id=aluno,
        data_inicio__date__range=(data_inicio, data_fim)
    )
    mensalidades_pagas = sum((m.mensalidade_paga or 0) for m in mensalidades)

    # Comparticipações deste aluno no periodo
    comparticoes = ComparticaoMensalSS.objects.filter(
        aluno_id=aluno,
        data_inicio__date__range=(data_inicio, data_fim)
    )
    comparticoes_pagas = sum((c.mensalidade_paga or 0) for c in comparticoes)

    balanco = mensalidades_pagas + comparticoes_pagas - custo_por_crianca

    SaudeFinanceiraBalancoAluno.objects.create(
        aluno_id=aluno,
        mensalidades_pagas_total=mensalidades_pagas,
        comparticoes_pagas_total=comparticoes_pagas,
        custo_por_crianca=custo_por_crianca,
        balanco=balanco,
        data_inicio=data_inicio,
        data_fim=data_fim
    )


# Funçoes para os filtros da saude financeira
def filtrosBalancoGlobal(request, saudes_financeiras_balanco_global):

    valoresSelecionadosGetFiltros = {}
    data_inicio_get = request.GET.get("data_inicio")
    data_fim_get = request.GET.get("data_fim")

    if data_inicio_get:
        saudes_financeiras_balanco_global = saudes_financeiras_balanco_global.filter(data_inicio__gte=data_inicio_get)
        valoresSelecionadosGetFiltros["data_inicio"] = data_inicio_get

    if data_fim_get:
        saudes_financeiras_balanco_global = saudes_financeiras_balanco_global.filter(data_fim__lte=data_fim_get)
        valoresSelecionadosGetFiltros["data_fim"] = data_fim_get

    return saudes_financeiras_balanco_global, valoresSelecionadosGetFiltros

def filtrosBalancoValencia(request, saudes_financeiras_balanco_valencia):

    valoresSelecionadosGetFiltros = {}
    data_inicio_get = request.GET.get("data_inicio")
    data_fim_get = request.GET.get("data_fim")
    valencia_get = request.GET.get("valencia")

    if data_inicio_get:
        saudes_financeiras_balanco_valencia = saudes_financeiras_balanco_valencia.filter(data_inicio__gte=data_inicio_get)
        valoresSelecionadosGetFiltros["data_inicio"] = data_inicio_get

    if data_fim_get:
        saudes_financeiras_balanco_valencia = saudes_financeiras_balanco_valencia.filter(data_fim__lte=data_fim_get)
        valoresSelecionadosGetFiltros["data_fim"] = data_fim_get

    if valencia_get:
        saudes_financeiras_balanco_valencia = saudes_financeiras_balanco_valencia.filter(valencia=valencia_get)
        valoresSelecionadosGetFiltros["valencia"] = valencia_get

    return saudes_financeiras_balanco_valencia, valoresSelecionadosGetFiltros

def filtrosBalancoEscalao(request, saudes_financeiras_balanco_escalao):

    valoresSelecionadosGetFiltros = {
        "data_inicio": None,
        "data_fim": None,
        "escalao": None
    }

    data_inicio_get = request.GET.get("data_inicio")
    data_fim_get = request.GET.get("data_fim")
    escalao_get = request.GET.get("escalao")

    if data_inicio_get:
        saudes_financeiras_balanco_escalao = saudes_financeiras_balanco_escalao.filter(data_inicio__gte=data_inicio_get)
        valoresSelecionadosGetFiltros["data_inicio"] = data_inicio_get

    if data_fim_get:
        saudes_financeiras_balanco_escalao = saudes_financeiras_balanco_escalao.filter(data_fim__lte=data_fim_get)
        valoresSelecionadosGetFiltros["data_fim"] = data_fim_get

    if escalao_get:
        saudes_financeiras_balanco_escalao = saudes_financeiras_balanco_escalao.filter(escalao=escalao_get)
        valoresSelecionadosGetFiltros["escalao"] = escalao_get

    return saudes_financeiras_balanco_escalao, valoresSelecionadosGetFiltros

def filtrosBalancoAluno(request, saudes_financeiras_balanco_aluno):

    valoresSelecionadosGetFiltros = {
        "data_inicio": None,
        "data_fim": None,
    }

    data_inicio_get = request.GET.get("data_inicio")
    data_fim_get = request.GET.get("data_fim")

    if data_inicio_get:
        saudes_financeiras_balanco_aluno = saudes_financeiras_balanco_aluno.filter(data_inicio__gte=data_inicio_get)
        valoresSelecionadosGetFiltros["data_inicio"] = data_inicio_get

    if data_fim_get:
        saudes_financeiras_balanco_aluno = saudes_financeiras_balanco_aluno.filter(data_fim__lte=data_fim_get)
        valoresSelecionadosGetFiltros["data_fim"] = data_fim_get

    return saudes_financeiras_balanco_aluno, valoresSelecionadosGetFiltros





# Saude financeira
@login_required
def show_saude_fianceira(request):

    form_type = request.POST.get("form_type")
    if request.method == "POST":
        match form_type:
            case "balanco_global":
                balancoGlobal(request)
            case "balanco_valencia":
                balancoValencia(request)
            case "balanco_escalao":
                balancoEscalao(request)
            case "balanco_aluno":
                balancoAluno(request)
            case _:
                print("Post incompativel")


    # Valores para aparecer na seleçao dos filtros
    valoresSelecaoFiltros = {
        "valencias": Sala.objects.values_list('sala_valencia', flat=True).distinct(),
        "escaloes": EscaloesRendimento.objects.values_list("escalao", flat = True).distinct(),
        "alunos": Aluno.objects.filter(archive_flag=False)
    }

    # Get
    valoresSelecionadosGetFiltros = {
        "balanco_global": {
            "data_inicio": None,
            "data_fim": None
        },
        "balanco_valencia": {
            "data_inicio": None,
            "data_fim": None,
            "valencia": None
        },
        "balanco_escalao": {
            "data_inicio": None,
            "data_fim": None,
            "escalao": None
        },
        "balanco_aluno": {
            "data_inicio": None,
            "data_fim": None,
        }

    }


    saudes_financeiras_balanco_global = SaudeFinanceiraBalancoGlobal.objects.all()
    saudes_financeiras_balanco_valencia = SaudeFinanceiraBalancoValencia.objects.all()
    saudes_financeiras_balanco_escalao = SaudeFinanceiraBalancoEscalao.objects.all()
    saudes_financeiras_balanco_aluno = SaudeFinanceiraBalancoAluno.objects.all()

    # Quem fez get
    form_type = request.GET.get("form_type")
    match form_type:
        case "balanco_global":
            saudes_financeiras_balanco_global, valoresSelecionadosGetFiltros["balanco_global"] = filtrosBalancoGlobal(request, saudes_financeiras_balanco_global)
        case "balanco_valencia":
            saudes_financeiras_balanco_valencia, valoresSelecionadosGetFiltros["balanco_valencia"] = filtrosBalancoValencia(request, saudes_financeiras_balanco_valencia)
            pass
        case "balanco_escalao":
            saudes_financeiras_balanco_escalao, valoresSelecionadosGetFiltros["balanco_escalao"] = filtrosBalancoEscalao(request, saudes_financeiras_balanco_escalao)
            pass
        case "balanco_aluno":
            saudes_financeiras_balanco_aluno, valoresSelecionadosGetFiltros["balanco_aluno"] = filtrosBalancoAluno(request, saudes_financeiras_balanco_aluno)
            pass
        case _:
            print("Get incompativel")




    contexto = {
        "saudesFinanceirasBalancoGlobal": saudes_financeiras_balanco_global,
        "saudes_financeiras_balanco_valencia": saudes_financeiras_balanco_valencia,
        "saudes_financeiras_balanco_escalao": saudes_financeiras_balanco_escalao,
        "saudes_financeiras_balanco_aluno": saudes_financeiras_balanco_aluno,
        "valoresSelecionadosGetFiltros": valoresSelecionadosGetFiltros,
        "valoresSelecaoFiltros": valoresSelecaoFiltros
    }

    return render(request, 'show_saude_financeira.html', contexto)

def delete_saude_financeira(request, tipo, balanco_id):
    modelos = {
        "global": SaudeFinanceiraBalancoGlobal,
        "valencia": SaudeFinanceiraBalancoValencia,
        "escalao": SaudeFinanceiraBalancoEscalao,
        "aluno": SaudeFinanceiraBalancoAluno,
    }

    modelo = modelos.get(tipo)
    if modelo is None:
        return HttpResponse("Tipo de balanço inválido", status=400)

    registo = get_object_or_404(modelo, pk=balanco_id)
    registo.delete()
    return redirect('show_saude_financeira')

def relatorio_pdf(request):

    form_type = request.GET.get("form_type")

    contexto = {
        "form_type": form_type,
        "gerado_em": timezone.now(),
        "filtros": {},
        "dados": []
    }

    # Aplica os mesmos filtros da pagina da saude financeira
    match form_type:
        case "balanco_global":
            contexto["titulo"] = "Relatório - Balanço Global"
            dados, filtros = filtrosBalancoGlobal(request, SaudeFinanceiraBalancoGlobal.objects.all())
        case "balanco_valencia":
            contexto["titulo"] = "Relatório - Balanço por Valência"
            dados, filtros = filtrosBalancoValencia(request, SaudeFinanceiraBalancoValencia.objects.all())
        case "balanco_escalao":
            contexto["titulo"] = "Relatório - Balanço por Escalão"
            dados, filtros = filtrosBalancoEscalao(request, SaudeFinanceiraBalancoEscalao.objects.all())
        case "balanco_aluno":
            contexto["titulo"] = "Relatório - Balanço por Aluno"
            dados, filtros = filtrosBalancoAluno(request, SaudeFinanceiraBalancoAluno.objects.all())
        case _:
            return HttpResponse("Tipo de relatório inválido", status=400)

    contexto["dados"] = dados
    contexto["filtros"] = filtros

    # Renderiza o template HTML e converte para PDF
    html = get_template('relatorio_pdf.html').render(contexto)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_financeiro.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response









# Autentificacao
def insert_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_active = False
            user.save()

            return redirect('starter_page')
        else:
            print(form.errors)
    else:
        form = UserForm()
    return render(request, 'insert_user.html', {'form': form})