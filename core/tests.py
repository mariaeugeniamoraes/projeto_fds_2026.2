from django.test import TestCase
from django.contrib.auth.models import User
from .forms import CadastroUsuarioForm


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
