from _datetime import datetime as dt
from django.shortcuts import redirect, render, get_object_or_404
from .forms import *
from .models import *
from .auto_gen_form_views import *
from django.utils.http import urlencode
from .auto_gen_id_views import *
from django.db.models import Q
from django.db.models import F, Value, CharField
from django.db.models.functions import Concat, Cast
from django.db import connection
from django.contrib import messages


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

    # Filtros
    has_filters = any(key in request.GET for key in ['nome', 'sala', 'mes', 'ano'])

    # Verefica se existe parametros para os filtros
    if not has_filters:
        filter_mes = dt.now().month
        filter_ano = dt.now().year
        filter_nome = ''
        filter_sala = ''
    else:
        filter_nome = request.GET.get('nome', '')
        filter_sala = request.GET.get('sala', '')
        filter_mes = request.GET.get('mes', '')
        filter_ano = request.GET.get('ano', '')
    ano_atual = dt.now().year
    meses_range = range(1, 13)
    anos_range = range(2000, ano_atual + 1)

    data_salas = Sala.objects.all()
    data_financas = AlunoFinancas.objects.annotate(
        Ano_letivo=F('ano_letivo'),
        Despesa_anual=F('despesa_anual'),
        Rendimento_líquido=F('rendim_líquido'),
        Nome=Concat(
            'aluno_id__nome_proprio',
            Value(' '),
            'aluno_id__apelido',
            output_field=CharField()),
        Documento=F('aluno_id__numero_documento')
    )
    data_mensalidade = MensalidadeAluno.objects.annotate(
        Data=Concat(
            'ano',
            Value('/'),
            'mes',
            output_field=CharField()
        ),
        Valor_a_pagar =F('mensalidade_calc'),
        Valor_pago = F('mensalidade_paga'),
        Data_Pagamento = Cast('data_pagamento', CharField()),
        Modo_Pagamento=F('modo_pagamento'),
        Serviço=F('programa_ss'),
        Acordo = F('acordo'),
        Nome=Concat(
            'aluno_id__nome_proprio',
            Value(' '),
            'aluno_id__apelido',
            output_field=CharField()),
        Sala = F('aluno_id__sala_id__sala_nome'),
        Data_Nascimento = Cast('aluno_id__data_nascimento', CharField()),
    ).order_by('-ano','mes')


    if request.method == "POST" and 'mensalidadeFinal' in request.POST:
        p_nome = request.POST.get('filter_nome', '')
        p_sala = request.POST.get('filter_sala', '')
        p_mes = request.POST.get('filter_mes') or dt.now().month
        p_ano = request.POST.get('filter_ano') or dt.now().year

        extra_filters = ""
        filter_params = []
        params_url = urlencode({
            'nome': p_nome,
            'sala': p_sala,
            'mes': p_mes,
            'ano': p_ano
        })

        if p_nome:
            extra_filters += " AND (a.nome_proprio || ' ' || a.apelido) LIKE %s"
            filter_params.append(f"%{p_nome}%")

        if p_sala:
            extra_filters += " AND s.sala_nome = %s"
            filter_params.append(p_sala)

        target_ano = p_ano if p_ano else dt.now().year
        target_mes = p_mes if p_mes else dt.now().month

        all_params = [target_ano, target_mes] + filter_params + [target_ano, target_mes]

        # Query do calculo da mensalidade
        queryMensalidade = f"""
                INSERT INTO mensalidade_aluno (
                    aluno_id,
                    ano,
                    mes,
                    mensalidade_calc,
                    mensalidade_retific,
                    mensalidade_paga,
                    data_pagamento,
                    modo_pagamento,
                    programa_ss,
                    acordo
                )
                SELECT
                    resultado.id,
                    %s,
                    %s,
                    ROUND(resultado.mensalidade_final,2 ),
                    NULL,
                    NULL,
                    NULL,
                    NULL,
                    NULL,
                    NULL
                FROM (
                         SELECT
                             calc.aluno_id AS id,
                             calc.rc AS rc,
                             e.perc_rend_per_capita AS limite_superior,
                             (calc.rc * (e.comparticipacao_da_familia / 100.0)) AS mensalidade_final
                         FROM (
                                  SELECT
                                      a.aluno_id,
                                      ((af.rendim_líquido - af.despesa_anual) / (12.0 * af.agregado)) AS rc,
                                      c.value As rmmg
                                  FROM aluno a
                                           LEFT JOIN aluno_financas af ON a.aluno_id = af.aluno_id
                                           LEFT JOIN config_ipss c ON c.key='RMMG' AND active_flag = 1
                                           LEFT JOIN sala s ON a.sala_id = s.sala_id
                                  WHERE 1=1 {extra_filters}
                              ) AS calc
                                  LEFT JOIN escaloes_rendim e ON (calc.rc / rmmg) * 100 <= e.perc_rend_per_capita
                         GROUP BY id
                         HAVING e.perc_rend_per_capita = MIN(e.perc_rend_per_capita)
                     ) AS resultado
                WHERE NOT EXISTS (
                    SELECT 1 FROM mensalidade_aluno m
                    WHERE m.aluno_id = resultado.id
                      AND m.ano = %s
                      AND m.mes = %s
                );
                """

        # Query calculo comparticoes
        queryComparticaoSS = f"""
                INSERT INTO comparticipacao_mensal_ss (
                aluno_id,
                aluno_mensalidade_id,
                ano_letivo,
                periodo_inicio,
                mensalidade_valor,
                programa_ss
                )
                SELECT 
                ma.aluno_id,
                ma.ma_id,
                ma.ano,
                CURRENT_DATE AS periodo_inicio,
                CASE 
                  WHEN a.comparticao_ss_custom IS NOT NULL THEN a.comparticao_ss_custom
                  ELSE p.custo
                END,
                p.nome AS programa_ss
                from mensalidade_aluno ma
                JOIN aluno a ON ma.aluno_id = a.aluno_id
                JOIN programa p ON a.programa_id = p.programa_id
                ON CONFLICT(aluno_mensalidade_id)
                DO UPDATE SET
                mensalidade_valor = excluded.mensalidade_valor,
                programa_ss = excluded.programa_ss,
                periodo_inicio = excluded.periodo_inicio;
                """

        # Exucutar as mudandças/querys
        try:
            with connection.cursor() as cursor:
                cursor.execute(queryMensalidade, all_params)
                cursor.execute(queryComparticaoSS)
                count = cursor.rowcount
                if count == 0:
                    messages.warning(request, f"Mensalidades já existem para {target_mes}/{target_ano}.")
                else:
                    messages.success(request, f"Sucesso! {count} mensalidades calculadas para {target_mes}/{target_ano}.")
        except Exception as e:
            messages.error(request, f"Erro: {e}")
        return redirect(f"{request.path}?{params_url}")

    # Aplica os filtros
    if filter_nome:
        data_mensalidade = data_mensalidade.filter(Nome__icontains=filter_nome)

    if filter_sala:
        data_mensalidade = data_mensalidade.filter(Sala__icontains=filter_sala)

    if filter_mes:
        data_mensalidade = data_mensalidade.filter(mes=filter_mes)

    if filter_ano:
        data_mensalidade = data_mensalidade.filter(ano=filter_ano)



    # Headers
    head_financas = [
        "Ano_letivo",
        "Despesa_anual",
        "Rendimento_líquido",
        "Nome",
        "Documento"
         ]
    head_mensalidade = [
        "Data",
        "Valor_a_pagar",
        "Valor_pago",
        "Data_Pagamento",
        "Modo_Pagamento",
        "Serviço",
        "Acordo",
        "Nome",
        "Sala",
        "Data_Nascimento",
        ]




    #
    filtersValue = {
        "sala": filter_sala,
        "nome": filter_nome,
        "mes": int(filter_mes) if str(filter_mes).isdigit() else None,
        "ano": int(filter_ano) if str(filter_ano).isdigit() else None,
    }

    data_financas = list(data_financas.values(*head_financas))
    data_mensalidade = list(data_mensalidade.values(*head_mensalidade))

    context = {
        "head_financas": head_financas,
        "data_financas": data_financas,
        "head_mensalidade": head_mensalidade,
        "data_mensalidade": data_mensalidade,
        "data_salas": data_salas,
        "meses_range": meses_range,
        "anos_range": anos_range,
        "filtersValue": filtersValue,
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