from django import forms
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