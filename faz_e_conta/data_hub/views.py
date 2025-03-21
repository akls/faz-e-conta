from django.shortcuts import redirect, render

from .forms import AlunoForm
from .models import Aluno
from .utils import dynamic_filter
from django.db.models import Q  # Import Q for dynamic filtering

def starter_page(request):
    return render(request, "starter_page.html")

def show_students(request):
    query = request.GET.get("q", "")  # Get search query from the URL
    if query:
        data = Aluno.objects.filter(
            Q(nome_proprio__icontains=query) | 
            Q(apelido__icontains=query) | 
            Q(processo__icontains=query)
        )  # Search across multiple fields
    else:
        data = Aluno.objects.all()
    # data = Aluno.objects.all()
    return render(request, "show_students.html", {"data": data,
                                                  "query": query})

def insert_student(request):
    if request.method == "POST":
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("show_students")
    else:
        form = AlunoForm()
    return render(request, "insert_student.html", {"form": form})