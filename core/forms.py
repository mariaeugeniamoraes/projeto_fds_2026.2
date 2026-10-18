from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Feedback, Empresa, RegistroFinanceiro


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

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'Este e-mail já está cadastrado. Utilize outro e-mail.'
            )

        return email


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


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ["nome", "cnpj", "setor"]
        labels = {
            "nome": "Nome da empresa",
            "cnpj": "CNPJ (opcional)",
            "setor": "Setor de atuação",
        }
        widgets = {
            "nome": forms.TextInput(attrs={
                "placeholder": "Ex.: Minha Loja Virtual"
            }),
            "cnpj": forms.TextInput(attrs={
                "placeholder": "00.000.000/0000-00"
            }),
            "setor": forms.TextInput(attrs={
                "placeholder": "Ex.: Moda, cosméticos, alimentos"
            }),
        }


MATERIAL_CHOICES = [
    ('plastico_bolha', 'Plástico bolha convencional'),
    ('fita_plastica', 'Fita adesiva plástica'),
    ('envelopes_plasticos', 'Envelopes/Sacos plásticos'),
    ('caixa_virgem', 'Caixa de papelão com fita plástica'),
]


class CalculadoraEmbalagemForm(forms.Form):
    material_atual = forms.ChoiceField(
        choices=MATERIAL_CHOICES,
        label="Material de embalagem atual",
        required=True
    )
    quantidade_mensal = forms.IntegerField(
        label="Quantidade utilizada por mês (unidades)",
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Ex: 1000'})
    )
    custo_unitario_atual = forms.DecimalField(
        label="Custo unitário atual (R$)",
        min_value=0.01,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Ex: 1.50'})
    )
class RegistroFinanceiroForm(forms.ModelForm):
    class Meta:
        model = RegistroFinanceiro
        fields = [
            "tipo",
            "descricao",
            "categoria",
            "valor",
            "data",
            "observacao",
        ]
        labels = {
            "tipo": "Tipo de movimentação",
            "descricao": "Descrição",
            "categoria": "Categoria",
            "valor": "Valor (R$)",
            "data": "Data da movimentação",
            "observacao": "Observações",
        }
        widgets = {
            "tipo": forms.Select(),
            "descricao": forms.TextInput(attrs={
                "placeholder": "Ex.: Venda de produtos"
            }),
            "categoria": forms.TextInput(attrs={
                "placeholder": "Ex.: Vendas, embalagens, logística"
            }),
            "valor": forms.NumberInput(attrs={
                "placeholder": "0,00",
                "step": "0.01",
                "min": "0.01",
            }),
            "data": forms.DateInput(attrs={
                "type": "date"
            }),
            "observacao": forms.Textarea(attrs={
                "placeholder": "Informações adicionais (opcional)",
                "rows": 3,
            }),
        }

from django import forms
from .models import PlanoAcaoESG

class PlanoAcaoForm(forms.ModelForm):
    class Meta:
        model = PlanoAcaoESG
        fields = ['titulo', 'descricao', 'prioridade', 'status']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Substituir plástico bolha'}),
            'descricao': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Descreva a ação...'}),
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

from django import forms
from .models import Fornecedor

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'servico', 'auditoria_pendente', 'contrato_assinado', 'tecidos_certificados']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Oficina de Costura Silva'}),
            'servico': forms.TextInput(attrs={'placeholder': 'Ex: Costura, Estamparia, Tecelagem'}),
            'auditoria_pendente': forms.CheckboxInput(),
            'contrato_assinado': forms.CheckboxInput(),
            'tecidos_certificados': forms.CheckboxInput(),
        }