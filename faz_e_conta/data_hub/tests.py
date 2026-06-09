import os
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import make_aware
from django.core.management import call_command
from django.contrib.auth.models import User
from datetime import datetime
from .models import Aluno, Sala, ResponsavelEducativo, Funcionario, programa


# RQ01
# Test case 1 - Criar conta de administrador com sucesso
class CriarSuperuserTest(TestCase):
    def test_criar_superuser(self):
        os.environ["DJANGO_SUPERUSER_PASSWORD"] = "admin123"
        call_command(
            "createsuperuser",
            interactive=False,
            username="admin",
            email="admin@faz-e-conta.pt",
        )

        
        admin = User.objects.get(username="admin")
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
        self.assertEqual(admin.email, "admin@faz-e-conta.pt")
        self.assertTrue(admin.check_password("admin123"))


# Test case 2 - Criar conta de utilizador comum (fica pendente de aprovação)
class CriarUtilizadorComumTest(TestCase):
    def test_utilizador_fica_pendente_e_login_bloqueado(self):
        # Passo 1: aceder ao formulario de registo
        response_get = self.client.get(reverse("insert_user"))
        self.assertEqual(response_get.status_code, 200)

        # Passo 2 e 3: preencher com dados validos e submeter
        response_post = self.client.post(reverse("insert_user"), {
            "username": "joao",
            "email": "joao@faz-e-conta.pt",
            "password": "segredo123",
        })

        # Resultado: conta criada
        self.assertEqual(User.objects.filter(username="joao").count(), 1)
        utilizador = User.objects.get(username="joao")

        # Resultado passo 3: conta criada com estado "Pendente" (inativa)
        self.assertFalse(utilizador.is_active)

        # Passo 4: tentar fazer login -> bloqueado porque a conta esta inativa
        login_ok = self.client.login(username="joao", password="segredo123")
        self.assertFalse(login_ok)


# Test case 3 - Aprovar conta de utilizador (via admin do Django)
class AprovarUtilizadorTest(TestCase):
    def setUp(self):
        # Administrador
        User.objects.create_superuser(
            username="admin", email="admin@faz-e-conta.pt", password="admin123"
        )
        # Utilizador comum pendente (inativo)
        self.utilizador = User.objects.create_user(
            username="joao", email="joao@faz-e-conta.pt", password="segredo123"
        )
        self.utilizador.is_active = False
        self.utilizador.save()

    def test_admin_aprova_utilizador(self):
        # Passo 1: login como administrador
        self.assertTrue(self.client.login(username="admin", password="admin123"))

        # Passo 2: aceder a lista de utilizadores no admin
        lista = self.client.get("/admin/auth/user/")
        self.assertEqual(lista.status_code, 200)
        self.assertContains(lista, "joao")

        # Passo 3: aprovar -> ativar o utilizador pelo formulario do admin
        resposta = self.client.post(
            f"/admin/auth/user/{self.utilizador.id}/change/",
            {
                "username": "joao",
                "email": "joao@faz-e-conta.pt",
                "first_name": "",
                "last_name": "",
                "is_active": "on",
                "date_joined_0": "2024-01-01",
                "date_joined_1": "10:00:00",
                "last_login_0": "",
                "last_login_1": "",
                "_save": "Save",
            },
        )
        self.assertEqual(resposta.status_code, 302)

        # Resultado: estado alterado para "Aprovado" (ativo)
        self.utilizador.refresh_from_db()
        self.assertTrue(self.utilizador.is_active)

        # Passo 4: utilizador ja consegue fazer login
        novo_cliente = Client()
        self.assertTrue(novo_cliente.login(username="joao", password="segredo123"))


# Test case 4 - Rejeitar conta de utilizador (via admin do Django)
class RejeitarUtilizadorTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(
            username="admin", email="admin@faz-e-conta.pt", password="admin123"
        )
        self.utilizador = User.objects.create_user(
            username="joao", email="joao@faz-e-conta.pt", password="segredo123"
        )
        self.utilizador.is_active = False
        self.utilizador.save()

    def test_admin_rejeita_utilizador(self):
        # Passo 1: login enquanto administrador
        self.assertTrue(self.client.login(username="admin", password="admin123"))

        # Passo 2: rejeitar -> remover a conta pendente via admin
        resposta = self.client.post(
            f"/admin/auth/user/{self.utilizador.id}/delete/",
            {"post": "yes"},
        )
        self.assertEqual(resposta.status_code, 302)

        # Resultado: conta deixou de existir (rejeitada)
        self.assertFalse(User.objects.filter(username="joao").exists())

        # Passo 3: utilizador tenta login -> bloqueado (conta ja nao existe)
        novo_cliente = Client()
        self.assertFalse(novo_cliente.login(username="joao", password="segredo123"))


# Test case 5 - Validacao do formulario de criacao de conta
class ValidacaoFormularioUtilizadorTest(TestCase):
    def test_formulario_apresentado(self):
        # Passo 1: aceder ao formulario -> apresentado corretamente
        response = self.client.get(reverse("insert_user"))
        self.assertEqual(response.status_code, 200)

    def test_campos_obrigatorios_em_falta(self):
        # Passo 2: submeter sem preencher os campos obrigatorios
        response = self.client.post(reverse("insert_user"), {})

        # Mensagens de erro exibidas (form reapresentado) e conta nao criada
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn("username", response.context["form"].errors)
        self.assertIn("password", response.context["form"].errors)

    def test_email_invalido(self):
        # Passo 3: inserir e-mail com formato invalido (resto preenchido)
        response = self.client.post(reverse("insert_user"), {
            "username": "joao",
            "password": "segredo123",
            "email": "isto-nao-e-email",
        })

        # Passo 4: sistema rejeita o formato e a conta nao e criada
        self.assertEqual(response.status_code, 200)
        self.assertIn("email", response.context["form"].errors)
        self.assertEqual(User.objects.count(), 0)









# RQ_F05
# Test case 1 (criar aluno via formulario)
class InsertAlunoTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.sala = Sala.objects.create(sala_nome="Sala A", sala_valencia="Valência 1")
        self.programa = programa.objects.create(nome="Creche", custo=100)
        self.responsavel = ResponsavelEducativo.objects.create(
            nome_proprio="Carlos",
            apelido="Oliveira",
            data_nascimento="1980-01-01",
            documento="CC",
            numero_documento=987654,
            data_validade="2035-01-01",
            morada="Rua das Flores",
            codigo_postal="1234-567",
            concelho="Lisboa",
            fregesia="Freguesia X",
        )

    def test_insert_aluno(self):
        # archive_flag é omitido
        response = self.client.post(reverse('insert_aluno_view'), {
            'nome_proprio': 'Maria',
            'apelido': 'Santos',
            'sala_id': self.sala.sala_id,
            'programa_id': self.programa.programa_id,
            'responsaveis_educativos_ids': [self.responsavel.responsavel_educativo_id],
            'data_admissao': '2023-01-01',
            'data_nascimento': '2010-01-01',
            'documento': 'BI',
            'numero_documento': '654321',
            'data_validade': '2030-01-01',
            'morada': 'Rua das Flores',
            'concelho': 'Lisboa',
            'codigo_postal': '1234-567',
            'fregesia': 'Freguesia X',
        })

        # Foi criado e redirecionou para a lista de alunos
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Aluno.objects.count(), 1)

        aluno = Aluno.objects.first()
        self.assertEqual(aluno.nome_proprio, 'Maria')
        self.assertEqual(aluno.apelido, 'Santos')
        self.assertEqual(aluno.sala_id, self.sala)
        self.assertEqual(aluno.programa_id, self.programa)
        self.assertFalse(aluno.archive_flag)
        self.assertIn(self.responsavel, aluno.responsaveis_educativos_ids.all())

# Test case 2 - Validacao do formulario de aluno
class AlunoFormValidacaoTest(TestCase):
    def setUp(self):
        self.sala = Sala.objects.create(sala_nome="Sala A", sala_valencia="Valência 1")
        self.programa = programa.objects.create(nome="Creche", custo=100)
        self.responsavel = ResponsavelEducativo.objects.create(
            nome_proprio="Carlos",
            apelido="Oliveira",
            data_nascimento="1980-01-01",
            documento="CC",
            numero_documento=987654,
            data_validade="2035-01-01",
            morada="Rua das Flores",
            codigo_postal="1234-567",
            concelho="Lisboa",
            fregesia="Freguesia X",
        )
        # Payload com todos os campos obrigatorios validos (base)
        self.dados_validos = {
            "nome_proprio": "Maria",
            "apelido": "Santos",
            "sala_id": self.sala.sala_id,
            "programa_id": self.programa.programa_id,
            "responsaveis_educativos_ids": [self.responsavel.responsavel_educativo_id],
            "data_admissao": "2023-01-01",
            "data_nascimento": "2010-01-01",
            "documento": "BI",
            "numero_documento": "654321",
            "data_validade": "2030-01-01",
            "morada": "Rua das Flores",
            "concelho": "Lisboa",
            "codigo_postal": "1234-567",
            "fregesia": "Freguesia X",
        }

    def test_formulario_apresentado(self):
        # Passo 1: aceder ao formulario
        response = self.client.get(reverse("insert_aluno_view"))
        self.assertEqual(response.status_code, 200)

    def test_campos_obrigatorios_em_falta(self):
        # Passo 2: submeter sem preencher nada
        response = self.client.post(reverse("insert_aluno_view"), {})

        # Mensagens de erro exibidas e aluno nao criado
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Aluno.objects.count(), 0)
        self.assertIn("nome_proprio", response.context["form"].errors)
        self.assertIn("apelido", response.context["form"].errors)

    def test_dados_invalidos(self):
        # Passo 3: tudo valido excepto a data de nascimento
        dados = self.dados_validos.copy()
        dados["data_nascimento"] = "data-invalida"

        response = self.client.post(reverse("insert_aluno_view"), dados)

        # Sistema rejeita o formato e o aluno nao e criado
        self.assertEqual(response.status_code, 200)
        self.assertIn("data_nascimento", response.context["form"].errors)
        self.assertEqual(Aluno.objects.count(), 0)

# Test case 3 - Inserir dados adicionais e confirmar que ficam visiveis
class AlunoDadosAdicionaisTest(TestCase):
    def setUp(self):
        self.sala = Sala.objects.create(sala_nome="Sala A", sala_valencia="Valência 1")
        self.programa = programa.objects.create(nome="Creche", custo=100)
        self.responsavel = ResponsavelEducativo.objects.create(
            nome_proprio="Carlos",
            apelido="Oliveira",
            data_nascimento="1980-01-01",
            documento="CC",
            numero_documento=987654,
            data_validade="2035-01-01",
            morada="Rua das Flores",
            codigo_postal="1234-567",
            concelho="Lisboa",
            fregesia="Freguesia X",
        )

    def test_dados_adicionais_guardados_e_visiveis(self):
        # Passo 1 e 2: preencher (incluindo dados adicionais opcionais) e submeter
        response = self.client.post(reverse("insert_aluno_view"), {
            "nome_proprio": "Maria",
            "apelido": "Santos",
            "sala_id": self.sala.sala_id,
            "programa_id": self.programa.programa_id,
            "responsaveis_educativos_ids": [self.responsavel.responsavel_educativo_id],
            "data_admissao": "2023-01-01",
            "data_nascimento": "2010-01-01",
            "documento": "BI",
            "numero_documento": "654321",
            "data_validade": "2030-01-01",
            "morada": "Rua das Flores",
            "concelho": "Lisboa",
            "codigo_postal": "1234-567",
            "fregesia": "Freguesia X",
            # dados adicionais
            "processo": "PROC-2026",
            "niss": 11122233,
            "nif": 99988877,
            "escolaridade_anterior": "1 Ciclo",
        })
        self.assertEqual(response.status_code, 302)

        # Passo 2 (resultado): dados guardados
        aluno = Aluno.objects.get(numero_documento="654321")
        self.assertEqual(aluno.processo, "PROC-2026")
        self.assertEqual(aluno.niss, 11122233)
        self.assertEqual(aluno.nif, 99988877)

        # Passo 3: consultar a pagina de detalhes -> informacao visivel
        detalhe = self.client.get(reverse("show_student_details", kwargs={"aluno_id": aluno.aluno_id}))
        self.assertEqual(detalhe.status_code, 200)
        self.assertContains(detalhe, "PROC-2026")








# RQ_F06
# Test case 1 - Criar encarregado de educacao com sucesso
class CriarEncarregadoTest(TestCase):
    def test_criar_encarregado(self):
        # Passo 1: aceder ao formulario
        get = self.client.get(reverse("insert_responsavel_educativo_view"))
        self.assertEqual(get.status_code, 200)

        # Passo 2 e 3: preencher com dados validos e submeter
        response = self.client.post(reverse("insert_responsavel_educativo_view"), {
            "nome_proprio": "Carlos",
            "apelido": "Oliveira",
            "data_nascimento": "1980-01-01",
            "documento": "CC",
            "numero_documento": 987654,
            "data_validade": "2035-01-01",
            "morada": "Rua das Flores",
            "codigo_postal": "1234-567",
            "concelho": "Lisboa",
            "fregesia": "Freguesia X",
        })

        # Resultado: encarregado criado com sucesso e gravado na BD
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ResponsavelEducativo.objects.count(), 1)
        encarregado = ResponsavelEducativo.objects.first()
        self.assertEqual(encarregado.nome_proprio, "Carlos")
        self.assertEqual(encarregado.apelido, "Oliveira")


# Test case 2 - Validacao do formulario do encarregado de educacao
class EncarregadoFormValidacaoTest(TestCase):
    def setUp(self):
        # Payload com todos os campos obrigatorios validos
        self.dados_validos = {
            "nome_proprio": "Carlos",
            "apelido": "Oliveira",
            "data_nascimento": "1980-01-01",
            "documento": "CC",
            "numero_documento": 987654,
            "data_validade": "2035-01-01",
            "morada": "Rua das Flores",
            "codigo_postal": "1234-567",
            "concelho": "Lisboa",
            "fregesia": "Freguesia X",
        }

    def test_formulario_apresentado(self):
        # Passo 1: aceder ao formulario
        response = self.client.get(reverse("insert_responsavel_educativo_view"))
        self.assertEqual(response.status_code, 200)

    def test_campos_obrigatorios_em_falta(self):
        # Passo 2: submeter sem preencher nada
        response = self.client.post(reverse("insert_responsavel_educativo_view"), {})

        # Mensagens de erro exibidas e encarregado nao criado
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ResponsavelEducativo.objects.count(), 0)
        self.assertIn("nome_proprio", response.context["form"].errors)
        self.assertIn("apelido", response.context["form"].errors)

    def test_dados_invalidos(self):
        # Passo 3: dados invalidos -> rejeita o formato.
        dados = self.dados_validos.copy()
        dados["numero_documento"] = "abc"

        response = self.client.post(reverse("insert_responsavel_educativo_view"), dados)

        # Passo 4: sistema rejeita e o encarregado nao e criado
        self.assertEqual(response.status_code, 200)
        self.assertIn("numero_documento", response.context["form"].errors)
        self.assertEqual(ResponsavelEducativo.objects.count(), 0)