from django.shortcuts import redirect, render
from .forms import AlunoForm
from .models import Aluno

def show_students(request):
    data = Aluno.objects.all()
    head = [field.name for field in Aluno._meta.fields]
    
    # Melhorando a criação da lista de dicionários
    data_dict = list(data.values(*head))
    
    return render(request, "show_students.html", {"data": data, "head": head, "data_dict": data_dict})

def insert_student(request):
    if request.method == "POST":
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("show_students")
    else:
        form = AlunoForm()
    
    return render(request, "insert_student.html", {"form": form})
