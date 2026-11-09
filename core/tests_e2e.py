
import os
import base64
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .models import Empresa, PassaporteProduto


# Evita problemas com o manifesto dos arquivos estáticos
# durante os testes, sem modificar a configuração de produção.
@override_settings(
    STORAGES={
        **settings.STORAGES,
        "staticfiles": {
            "BACKEND": (
                "django.contrib.staticfiles.storage.StaticFilesStorage"
            ),
        },
    }
)
class EcomplyE2ETest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        opcoes = Options()

        # No GitHub Actions, executa sem abrir janela.
        if os.getenv("CI", "").lower() == "true":
            opcoes.add_argument("--headless=new")

        opcoes.add_argument("--no-sandbox")
        opcoes.add_argument("--disable-dev-shm-usage")
        opcoes.add_argument("--window-size=1366,900")

        cls.navegador = webdriver.Chrome(options=opcoes)

    @classmethod
    def tearDownClass(cls):
        cls.navegador.quit()
        super().tearDownClass()

    def setUp(self):
        Usuario = get_user_model()

        # Cria um usuário no banco temporário de testes.
        self.usuario = Usuario.objects.create_user(
            username="usuario_teste_e2e",
            email="teste@example.com",
            password="SenhaSegura123!"
        )

        # Autentica o usuário no cliente Django.
        self.client.force_login(self.usuario)

        # Abre o servidor temporário no navegador.
        self.navegador.get(self.live_server_url)

        # Transfere a sessão autenticada para o Chrome.
        cookie = self.client.cookies[
            settings.SESSION_COOKIE_NAME
        ]

        self.navegador.add_cookie({
            "name": settings.SESSION_COOKIE_NAME,
            "value": cookie.value,
            "path": "/",
        })

    def fechar_aviso_privacidade(self):
        """
        Fecha o aviso de privacidade, se estiver visível.
        """

        botoes = self.navegador.find_elements(
            By.ID, "btn-entendi"
        )

        if botoes and botoes[0].is_displayed():

            WebDriverWait(
                self.navegador, 10
            ).until(
                EC.element_to_be_clickable(
                    (By.ID, "btn-entendi")
                )
            ).click()

            WebDriverWait(
                self.navegador, 10
            ).until(
                EC.invisibility_of_element_located(
                    (By.ID, "btn-entendi")
                )
            )

    def rolar_ate_elemento(self, elemento):
        """
        Rola a página e aguarda o elemento ficar
        dentro da área visível do navegador.
        """

        self.navegador.execute_script(
            "arguments[0].scrollIntoView({"
            "behavior: 'instant', "
            "block: 'center'"
            "});",
            elemento
        )

        WebDriverWait(
            self.navegador, 10
        ).until(
            lambda driver: driver.execute_script(
                """
                const rect = arguments[0]
                    .getBoundingClientRect();

                return (
                    rect.top >= 0 &&
                    rect.bottom <= window.innerHeight
                );
                """,
                elemento
            )
        )

    # ==================================================
    # TESTE 1 - DETECTOR DE GREENWASHING
    # ==================================================

    def test_detectar_greenwashing(self):
        """
        Testa a análise de alegações ambientais.
        """

        # Confirma que a página funciona no Django.
        resposta = self.client.get(
            reverse("detector_greenwashing")
        )

        self.assertEqual(resposta.status_code, 200)

        # Abre o Detector no Selenium.
        url = (
            self.live_server_url
            + reverse("detector_greenwashing")
        )

        self.navegador.get(url)

        # Fecha o aviso de privacidade.
        self.fechar_aviso_privacidade()

        # Aguarda o campo de propaganda aparecer.
        campo = WebDriverWait(
            self.navegador, 10
        ).until(
            EC.visibility_of_element_located(
                (By.NAME, "texto")
            )
        )

        # Digita uma propaganda com alegações suspeitas.
        campo.send_keys(
            "Nosso produto é 100% ecológico "
            "e totalmente sustentável."
        )

        # Localiza o botão de análise.
        botao = WebDriverWait(
            self.navegador, 10
        ).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".greenwashing-botao")
            )
        )

        # Rola até o botão.
        self.rolar_ate_elemento(botao)

        # Aguarda o botão estar clicável.
        botao = WebDriverWait(
            self.navegador, 10
        ).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".greenwashing-botao")
            )
        )

        # Envia a propaganda.
        botao.click()

        # Aguarda o resultado da análise.
        resultado = WebDriverWait(
            self.navegador, 10
        ).until(
            EC.visibility_of_element_located(
                (By.ID, "resultado-greenwashing")
            )
        )

        # Confirma que a análise foi concluída.
        self.assertIn(
            "Análise concluída",
            resultado.text
        )

        # Confirma as expressões encontradas.
        self.assertIn(
            "100% ecológico",
            resultado.text
        )

        self.assertIn(
            "totalmente sustentável",
            resultado.text
        )

        print("\nTeste do Detector de Greenwashing: OK")

    # ==================================================
    # TESTE 2 - PASSAPORTE DIGITAL
    # ==================================================

    def test_cadastrar_passaporte_digital(self):
        """
        Testa o cadastro, QR Code e página pública
        do Passaporte Digital de Sustentabilidade.
        """

        # Cria uma empresa vinculada ao usuário.
        empresa = Empresa.objects.create(
            usuario=self.usuario,
            nome="Empresa Sustentável de Teste"
        )

        # Armazena os QR Codes em uma pasta temporária.
        with tempfile.TemporaryDirectory() as pasta_media:
            with override_settings(MEDIA_ROOT=pasta_media):

                # Abre o formulário de cadastro.
                url = (
                    self.live_server_url
                    + reverse(
                        "passaporte_criar",
                        kwargs={"empresa_id": empresa.id}
                    )
                )

                self.navegador.get(url)

                # Fecha o aviso de privacidade.
                self.fechar_aviso_privacidade()

                # Aguarda o formulário carregar.
                campo_nome = WebDriverWait(
                    self.navegador, 10
                ).until(
                    EC.visibility_of_element_located(
                        (By.ID, "nome_produto")
                    )
                )

                # Preenche os dados do produto.
                campo_nome.send_keys(
                    "Camiseta Sustentável de Teste"
                )

                self.navegador.find_element(
                    By.ID, "descricao"
                ).send_keys(
                    "Produto cadastrado pelo Selenium."
                )

                self.navegador.find_element(
                    By.ID, "materiais"
                ).send_keys(
                    "80% algodão reciclado, 20% poliéster."
                )

                self.navegador.find_element(
                    By.ID, "origem_materiais"
                ).send_keys(
                    "Fornecedores brasileiros."
                )

                self.navegador.find_element(
                    By.ID, "embalagem"
                ).send_keys(
                    "Embalagem de papelão."
                )

                self.navegador.find_element(
                    By.ID, "instrucoes_descarte"
                ).send_keys(
                    "Separar a embalagem para "
                    "coleta seletiva de papel."
                )

                self.navegador.find_element(
                    By.ID, "indicadores_ambientais"
                ).send_keys(
                    "Informações ambientais de teste."
                )

                # Localiza o botão de cadastro.
                botao = WebDriverWait(
                    self.navegador, 10
                ).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".btn-submit")
                    )
                )

                # Rola até o botão, aguardando sua posição.
                self.rolar_ate_elemento(botao)

                # Aguarda o botão ficar clicável.
                botao = WebDriverWait(
                    self.navegador, 10
                ).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, ".btn-submit")
                    )
                )

                # Envia o formulário do produto.
                botao.click()

                # Aguarda o redirecionamento para a lista.
                WebDriverWait(
                    self.navegador, 10
                ).until(
                    EC.url_contains(
                        reverse("passaporte_lista")
                    )
                )

                # Confirma que o passaporte foi salvo.
                passaporte = PassaporteProduto.objects.get(
                    empresa=empresa,
                    nome_produto="Camiseta Sustentável de Teste"
                )

                self.assertEqual(
                    passaporte.materiais,
                    "80% algodão reciclado, 20% poliéster."
                )

                # Verifica se o QR Code foi gerado.
                self.assertTrue(
                    passaporte.qr_code.name,
                    "O passaporte não possui QR Code."
                )

                # Verifica se o arquivo de imagem existe.
                self.assertTrue(
                    passaporte.qr_code.storage.exists(
                        passaporte.qr_code.name
                    ),
                    "O arquivo do QR Code não foi encontrado."
                )

                # Monta a URL pública do passaporte.
                url_publica = (
                    self.live_server_url
                    + reverse(
                        "passaporte_publico",
                        kwargs={
                            "passaporte_id": passaporte.id
                        }
                    )
                )

                # Abre a página pública.
                self.navegador.get(url_publica)

                # Aguarda o nome do produto aparecer.
                WebDriverWait(
                    self.navegador, 10
                ).until(
                    EC.text_to_be_present_in_element(
                        (By.TAG_NAME, "body"),
                        "Camiseta Sustentável de Teste"
                    )
                )

                # Confirma que o produto aparece no relatório.
                texto_pagina = self.navegador.find_element(
                    By.TAG_NAME, "body"
                ).text

                self.assertIn(
                    "Camiseta Sustentável de Teste",
                    texto_pagina
                )

                print("\nTeste do Passaporte Digital: OK")

    # ==================================================
    # TESTE 3 - EXPORTAÇÃO DO DASHBOARD EM PDF
    # ==================================================

    def test_exportar_dashboard_pdf(self):
        """
        Testa a abertura do relatório ESG e sua
        conversão em PDF pelo navegador Chrome.
        """

        # Cria uma empresa para o usuário autenticado.
        empresa = Empresa.objects.create(
            usuario=self.usuario,
            nome="Empresa ESG de Teste"
        )

        # Monta a rota oficial do relatório.
        url_relatorio = reverse(
            "relatorio_empresa",
            kwargs={"empresa_id": empresa.id}
        )

        # Confirma que o relatório responde corretamente.
        resposta = self.client.get(url_relatorio)

        self.assertEqual(
            resposta.status_code,
            200
        )

        # Verifica se o relatório contém o nome da empresa.
        self.assertContains(
            resposta,
            "Empresa ESG de Teste"
        )

        # Abre o Dashboard no Selenium.
        url_dashboard = (
            self.live_server_url
            + reverse("dashboard")
        )

        self.navegador.get(url_dashboard)

        # Fecha o aviso de privacidade.
        self.fechar_aviso_privacidade()

        # Localiza o link Exportar PDF.
        seletor = (
            'a[href="' + url_relatorio + '"]'
        )

        botao = WebDriverWait(
            self.navegador, 10
        ).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, seletor)
            )
        )

        # Posiciona o link dentro da janela.
        self.rolar_ate_elemento(botao)

        # Aguarda o link ficar clicável.
        botao = WebDriverWait(
            self.navegador, 10
        ).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, seletor)
            )
        )

        # Guarda as abas que já estão abertas.
        aba_original = self.navegador.current_window_handle
        abas_antes = set(self.navegador.window_handles)

        try:
            # Clica em Exportar PDF.
            botao.click()

            # Aguarda a abertura de uma nova aba.
            WebDriverWait(
                self.navegador, 10
            ).until(
                lambda driver: len(
                    set(driver.window_handles) - abas_antes
                ) == 1
            )

            # Identifica a nova aba.
            nova_aba = (
                set(self.navegador.window_handles)
                - abas_antes
            ).pop()

            self.navegador.switch_to.window(nova_aba)

            # Aguarda o relatório carregar.
            WebDriverWait(
                self.navegador, 10
            ).until(
                EC.text_to_be_present_in_element(
                    (By.TAG_NAME, "body"),
                    "Empresa ESG de Teste"
                )
            )

            # Confirma que abriu a rota correta.
            self.assertIn(
                url_relatorio,
                self.navegador.current_url
            )

            # Converte a página HTML para PDF
            # usando o recurso de impressão do Chrome.
            resultado_pdf = (
                self.navegador.execute_cdp_cmd(
                    "Page.printToPDF",
                    {
                        "printBackground": True,
                        "preferCSSPageSize": True
                    }
                )
            )

            # Decodifica o arquivo PDF.
            conteudo_pdf = base64.b64decode(
                resultado_pdf["data"]
            )

            # Confirma a assinatura de um arquivo PDF.
            self.assertTrue(
                conteudo_pdf.startswith(b"%PDF-"),
                "O Chrome não gerou um PDF válido."
            )

            # Confirma que o PDF possui conteúdo.
            self.assertGreater(
                len(conteudo_pdf),
                100,
                "O PDF gerado está vazio."
            )

            print("\nTeste da Exportação do Dashboard: OK")

        finally:
            # Fecha as abas abertas durante o teste.
            for aba in self.navegador.window_handles:
                if aba not in abas_antes:
                    self.navegador.switch_to.window(aba)
                    self.navegador.close()

            # Volta para a aba original.
            self.navegador.switch_to.window(aba_original)
