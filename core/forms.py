from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Feedback


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback

        fields = ['nota', 'comentario']

        widgets = {
            'nota': forms.Select(
                choices=[
                    (1, '1 - Muito ruim'),
                    (2, '2 - Ruim'),
                    (3, '3 - Regular'),
                    (4, '4 - Bom'),
                    (5, '5 - Excelente'),
                ]
            ),

            'comentario': forms.Textarea(
                attrs={
                    'placeholder': 'Conte para nós o que achou do Ecomply...',
                    'rows': 5
                }
            ),
        }


class CadastroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(
        label='Nome',
        max_length=150,
        required=True
    )

    last_name = forms.CharField(
        label='Sobrenome',
        max_length=150,
        required=True
    )

    email = forms.EmailField(
        label='E-mail',
        required=True
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

class EditarUsuarioForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Nome',
        max_length=150,
        required=True
    )

    last_name = forms.CharField(
        label='Sobrenome',
        max_length=150,
        required=True
    )

    email = forms.EmailField(
        label='E-mail',
        required=True
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]