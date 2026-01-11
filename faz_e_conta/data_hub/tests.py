from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Aluno, Sala, ResponsavelEducativo, Funcionario

class AlunoModelTest(TestCase):
    def setUp(self):
        self.sala = Sala.objects.create(sala_nome="Sala A", sala_valencia="Valência 1")
        self.aluno = Aluno.objects.create(
            nome_proprio="João",
            apelido="Silva",
            sala_id=self.sala,
            data_admissao=make_aware(datetime(2023, 1, 1)),
            data_nascimento=make_aware(datetime(2010, 1, 1)),
            documento="BI",
            numero_documento="123456",
            data_validade=make_aware(datetime(2030, 1, 1)),
        )

    def test_aluno_str(self):
        self.assertEqual(str(self.aluno), "João Silva, Aluno Id: 1")

class ShowStudentsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.sala = Sala.objects.create(sala_nome="Sala A", sala_valencia="Valência 1")
        Aluno.objects.create(
            nome_proprio="João",
            apelido="Silva",
            sala_id=self.sala,
            data_admissao=make_aware(datetime(2023, 1, 1)),
            data_nascimento=make_aware(datetime(2010, 1, 1)),
            documento="BI",
            numero_documento="123456",
            data_validade=make_aware(datetime(2030, 1, 1)),
        )

    def test_show_students_view(self):
        response = self.client.get(reverse('show_students'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "João")
        self.assertContains(response, "Silva")

class ShowSalasViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        Sala.objects.create(sala_nome="Sala A", sala_valencia="Valência 1")
        Sala.objects.create(sala_nome="Sala B", sala_valencia="Valência 2")

    def test_show_salas_view(self):
        response = self.client.get(reverse('show_salas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sala A")
        self.assertContains(response, "Valência 1")

class InsertAlunoTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.sala = Sala.objects.create(sala_nome="Sala A", sala_valencia="Valência 1")

    def test_insert_aluno(self):
        response = self.client.post(reverse('insert_aluno_view'), {
            'nome_proprio': 'Maria',
            'apelido': 'Santos',
            'sala_id': self.sala.sala_id,
            'archive_flag': '0',
            'data_admissao': '2023-01-01T00:00:00Z',
            'data_nascimento': '2010-01-01T00:00:00Z',
            'documento': 'BI',
            'numero_documento': '654321',
            'data_validade': '2030-01-01T00:00:00Z',
            'morada': 'Rua das Flores',
            'concelho': 'Lisboa',
            'codigo_postal': '1234-567',
        })
        self.assertEqual(Aluno.objects.count(), 1)
        self.assertEqual(Aluno.objects.first().nome_proprio, 'Maria')
        
class InsertResponsavelEducativoTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.sala = Sala.objects.create(sala_nome="Sala A", sala_valencia="Valência 1")
        self.aluno = Aluno.objects.create(
            nome_proprio="João",
            apelido="Silva",
            sala_id=self.sala,
            data_admissao=make_aware(datetime(2023, 1, 1)),
            data_nascimento=make_aware(datetime(2010, 1, 1)),
            documento="BI",
            numero_documento="123456",
            data_validade=make_aware(datetime(2030, 1, 1)),
            morada="Rua das Flores",
            codigo_postal="1234-567",
            concelho="Lisboa",
        )

    def test_insert_responsavel_educativo(self):
        response = self.client.post(reverse('insert_responsavel_educativo_view'), {
            'nome_proprio': 'Carlos',
            'apelido': 'Oliveira',
            'aluno_id': self.aluno.aluno_id,
            'data_nascimento': '1980-01-01',
            'documento': 'CC',
            'numero_documento': '987654',
            'data_validade': '2035-01-01',
            'morada': 'Rua das Flores',
            'codigo_postal': '1234-567',
            'concelho': 'Lisboa',
            'fregesia': 'Freguesia X',
        })
        self.assertEqual(ResponsavelEducativo.objects.count(), 1)
        self.assertEqual(ResponsavelEducativo.objects.first().nome_proprio, 'Carlos')

class InsertFuncionarioTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_insert_funcionario(self):
        response = self.client.post(reverse('insert_funcionario_view'), {
            'nome_proprio': 'Ana',
            'apelido': 'Pereira',
            'data_nascimento': make_aware(datetime(1990, 1, 1)),
            'tipo_documento_identificacao': 'CC',
            'numero_documento_identificacao': '123456789',
            'data_validade': make_aware(datetime(2030, 1, 1)),
            'niss': 123456789,
            'nif': 987654321,
            'morada': 'Rua das Flores',
            'codigo_postal': '1234-567',
            'concelho': 'Lisboa',
            'contacto_telefonico': '912345678',
            'email': 'ana.pereira@example.com',
            'funcao': 'Educadora',
        })
        self.assertEqual(Funcionario.objects.count(), 1)
        self.assertEqual(Funcionario.objects.first().nome_proprio, 'Ana')