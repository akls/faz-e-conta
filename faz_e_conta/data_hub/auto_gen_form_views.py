from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import *

def insert_aluno_view(request):
    if request.method == "POST":
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_students')  # Redirect to the students list page
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
        form = Responsavel_educativoForm()
    return render(request, 'insert_responsavel_educativo.html', {'form': form})

