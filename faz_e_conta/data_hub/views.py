from django.shortcuts import redirect, render
from .forms import AlunoForm
from .models import Aluno

def show_students(request):
    data = Aluno.objects.all()
    #head = [field.name for field in Aluno._meta.fields]
    
    head = ["aluno_id", "nome_proprio", "apelido", "processo", "numero_documento", "data_admissao"]
    
    # Melhorando a criação da lista de dicionários
    data_dict = list(data.values(*head))
    
    return render(request, "show_students.html", {"head": head, "data_dict": data_dict, "id": head[0]})




def show_student(request, aluno_id):
    data = Aluno.objects.get(aluno_id=aluno_id)
    head = [field.name for field in Aluno._meta.fields]
    #head = ["aluno_id", "nome_proprio", "apelido"]
    data_dict = {head[i]: data.__dict__[head[i]] for i in range(1, len(head))}
    
    return render(request, "show_student.html", {"head": head, "data_dict": data_dict, "data":data, "id": head[0]})


def insert_student(request):
    if request.method == "POST":
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("show_students")
    else:
        form = AlunoForm()
    
    return render(request, "insert_student.html", {"form": form})
