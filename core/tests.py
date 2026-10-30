from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Empresa, DiagnosticoESG
from .forms import CadastroUsuarioForm
from django.test import override_settings

class CadastroUsuarioFormTest(TestCase):

    def setUp(self):
        User.objects.create_user(
            username='usuario1',
            email='teste@email.com',
            password='SenhaSegura123!'
        )

    def test_email_duplicado(self):
        form = CadastroUsuarioForm(data={
            'username': 'usuario2',
            'first_name': 'Maria',
            'last_name': 'Silva',
            'email': 'teste@email.com',
            'password1': 'OutraSenha123!',
            'password2': 'OutraSenha123!'
        })

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_email_novo(self):
        form = CadastroUsuarioForm(data={
            'username': 'usuario2',
            'first_name': 'Maria',
            'last_name': 'Silva',
            'email': 'novo@email.com',
            'password1': 'OutraSenha123!',
            'password2': 'OutraSenha123!'
        })

        self.assertTrue(form.is_valid())
@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage"
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        }
    }
)

class PortalTransparenciaTests(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username="testeportal",
            password="SenhaTeste123!"
        )

        self.empresa = Empresa.objects.create(
            usuario=self.usuario,
            nome="ConectaShop",
            setor="Moda"
        )

        self.diagnostico = DiagnosticoESG.objects.create(
            empresa=self.empresa,
            percentual_geral=66.67,
            percentual_ambiental=66.67,
            percentual_social=66.67,
            percentual_governanca=66.67,
            concluido=True
        )

        self.url = reverse(
            "portal_transparencia",
            args=[self.empresa.id]
        )

    def test_empresa_privada_nao_aparece(self):
        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 404)

    def test_empresa_publica_aparece(self):
        self.empresa.publicar_resultados = True
        self.empresa.save()

        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "ConectaShop")

    def test_usuario_pode_publicar_empresa(self):
        self.client.force_login(self.usuario)

        url = reverse(
            "alterar_publicacao_esg",
            args=[self.empresa.id]
        )

        resposta = self.client.post(url)

        self.empresa.refresh_from_db()

        self.assertTrue(self.empresa.publicar_resultados)
        self.assertEqual(resposta.status_code, 302)

    def test_usuario_pode_retirar_publicacao(self):
        self.empresa.publicar_resultados = True
        self.empresa.save()

        self.client.force_login(self.usuario)

        url = reverse(
            "alterar_publicacao_esg",
            args=[self.empresa.id]
        )

        self.client.post(url)

        self.empresa.refresh_from_db()

        self.assertFalse(self.empresa.publicar_resultados)

    def test_outro_usuario_nao_pode_alterar_publicacao(self):
        outro_usuario = User.objects.create_user(
            username="outro",
            password="SenhaTeste123!"
        )

        self.client.force_login(outro_usuario)

        url = reverse(
            "alterar_publicacao_esg",
            args=[self.empresa.id]
        )

        resposta = self.client.post(url)

        self.assertEqual(resposta.status_code, 404)

        self.empresa.refresh_from_db()
        self.assertFalse(self.empresa.publicar_resultados)


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage"
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        }
    }
)
class PainelAdminTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="adminteste",
            email="admin@email.com",
            password="SenhaTeste123!"
        )

        self.comum = User.objects.create_user(
            username="comum",
            email="comum@email.com",
            password="SenhaTeste123!"
        )

        Empresa.objects.create(
            usuario=self.comum,
            nome="Loja do Comum",
            setor="Moda"
        )

        self.url_painel = reverse("painel_admin")
        self.url_usuario = reverse("admin_usuario", args=[self.comum.id])

    def test_visitante_recebe_404(self):
        self.assertEqual(self.client.get(self.url_painel).status_code, 404)
        self.assertEqual(self.client.get(self.url_usuario).status_code, 404)

    def test_usuario_comum_recebe_404(self):
        self.client.force_login(self.comum)

        self.assertEqual(self.client.get(self.url_painel).status_code, 404)
        self.assertEqual(self.client.get(self.url_usuario).status_code, 404)

    def test_superuser_acessa_painel(self):
        self.client.force_login(self.admin)

        resposta = self.client.get(self.url_painel)

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "comum")
        self.assertEqual(resposta.context["resumo"]["usuarios"], 2)
        self.assertEqual(resposta.context["resumo"]["empresas"], 1)

    def test_painel_nao_exibe_email(self):
        self.client.force_login(self.admin)

        resposta = self.client.get(self.url_painel)

        self.assertNotContains(resposta, "comum@email.com")

    def test_detalhe_mostra_empresas_do_usuario(self):
        self.client.force_login(self.admin)

        resposta = self.client.get(self.url_usuario)

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Loja do Comum")
        self.assertNotContains(resposta, "comum@email.com")

    def test_menu_mostra_painel_so_para_superuser(self):
        self.client.force_login(self.comum)
        self.assertNotContains(self.client.get(reverse("home")), self.url_painel)

        self.client.force_login(self.admin)
        self.assertContains(self.client.get(reverse("home")), self.url_painel)
