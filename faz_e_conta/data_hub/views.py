from django.shortcuts import redirect, render

from .forms import AlunoForm
from .models import Aluno


def show_students(request):
    data = Aluno.objects.all()
    return render(request, "show_students.html", {"data": data})

def insert_student(request):
    if request.method == "POST":
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("show_students")
    else:
        form = AlunoForm()
    return render(request, "insert_student.html", {"form": form})