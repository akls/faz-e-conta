from django.shortcuts import render


from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .reports.reports import *
from .models import *
from .urls import *
from django.urls import get_resolver


login_url='login'
# Create your views here.

@login_required(login_url=login_url)
def index(request, counter: int = 2):
    imagens = Imagem.objects.all()
    graficos = [imagem.imagem.url for imagem in imagens if imagem.imagem.name.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Check if the request is from a mobile
    if request.META.get('HTTP_USER_AGENT'):
        user_agent = request.META['HTTP_USER_AGENT'].lower()
        if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
            counter = 1

    return render(request, "index.html", {
        "counter": counter,
        "graficos": graficos
    })

@login_required(login_url=login_url)
def reports(request):
    content = {
        'title': 'Reports',
        'description': 'This is the reports page.',
        'data': []
    }
    return render(request, 'financas/reports.html', content)


# User
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.groups.filter(name='Pendente').exists() and not user.is_staff and not user.is_superuser:
                messages.error(request, 'O utilizador está pendente de aprovação.')
            else:
                login(request, user)
                return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url=login_url)
def user_management(request):
    return render(request, 'user/management.html')

# Alunos
@login_required(login_url=login_url)
def dashboard_alunos(request):
    content = {
        'title': 'Dashboard Alunos',
        'valencia': gerar_grafico_numero_alunos_por_valencia(),
        'sala': gerar_grafico_alunos_por_sala(),
    }
    return render(request, 'alunos/dashboard.html', content)

@login_required(login_url=login_url)
def galeria(request):
    imagens_por_tipo = {}
    imagens = Imagem.objects.prefetch_related('tipo_imagem_id').all()

    for imagem in imagens:
        for tipo in imagem.tipo_imagem_id.all():
            tipo_nome = tipo.tipo_imagem
            if tipo_nome not in imagens_por_tipo:
                imagens_por_tipo[tipo_nome] = []
            imagens_por_tipo[tipo_nome].append(imagem)
    counter = 3
    # Check if the request is from a mobile
    if request.META.get('HTTP_USER_AGENT'):
        user_agent = request.META['HTTP_USER_AGENT'].lower()
        if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
            counter = 1
    content = {
        'imagens_por_tipo': imagens_por_tipo,
        'counter': counter,
    }
    return render(request, 'testes/galeria.html', content)



