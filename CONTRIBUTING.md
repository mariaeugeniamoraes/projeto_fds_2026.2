# Como contribuir com o Ecomply

Obrigado pelo interesse em contribuir com o **Ecomply**! O projeto é uma plataforma web desenvolvida em **Python e Django** para ajudar pequenas e médias empresas a acompanhar e melhorar práticas ambientais, sociais e de governança (ESG).

Este guia explica como conhecer o projeto, configurar um ambiente local, propor melhorias e enviar alterações para análise pela equipe.

## 1. Antes de começar

Para contribuir, você precisará de:

- **Git** instalado;
- **Python** e `pip` instalados (prefira uma versão compatível com as dependências do repositório);
- um editor de código, como o **Visual Studio Code**;
- uma conta no **GitHub** para enviar contribuições.

Conhecimentos básicos de Python, Django, HTML, CSS e JavaScript são úteis, mas sugestões de documentação, acessibilidade e testes também são bem-vindas.

## 2. Conheça a organização do projeto

Os principais caminhos do repositório são:

```text
projeto_fds_2026.2/
├── core/                 # Aplicação Django: modelos, views, URLs, testes e templates
├── ecomply/              # Configurações principais do projeto Django
├── manage.py             # Comandos de gerenciamento Django
├── requirements.txt      # Dependências Python
├── README.md             # Apresentação e documentação do projeto
└── CONTRIBUTING.md       # Este guia
```

Antes de alterar uma funcionalidade, identifique os arquivos correspondentes e verifique se outra pessoa já está trabalhando nela.

## 3. Configure o projeto no seu computador

### 3.1. Obtenha o código

Para contribuir como pessoa externa à equipe, faça primeiro um **fork** do repositório no GitHub. Depois, clone o seu fork (substitua `SEU_USUARIO` pelo nome da sua conta):

```bash
git clone https://github.com/SEU_USUARIO/projeto_fds_2026.2.git
cd projeto_fds_2026.2
```

Se você tem acesso autorizado ao repositório original, também pode cloná-lo diretamente:

```bash
git clone https://github.com/mariaeugeniamoraes/projeto_fds_2026.2.git
cd projeto_fds_2026.2
```

### 3.2. Crie e ative um ambiente virtual

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3.3. Instale as dependências

```bash
python -m pip install -r requirements.txt
```

### 3.4. Configure as variáveis de ambiente necessárias

O projeto pode depender de configurações locais, como chave secreta do Django, banco de dados e serviços externos. **Consulte o `README.md` e o arquivo de configurações em `ecomply/settings.py` para identificar as variáveis exigidas pela versão atual.**

Nunca coloque senhas, tokens, chaves de API ou outros segredos no código nem em commits. Se precisar de uma credencial de desenvolvimento, solicite orientações à equipe mantenedora.

### 3.5. Prepare o banco de dados e execute o site

Depois de configurar o ambiente e o banco compatível com o projeto, execute:

```bash
python manage.py migrate
python manage.py check
python manage.py runserver
```

Acesse o endereço local informado no terminal (normalmente `http://127.0.0.1:8000/`).

> **Observação:** se a configuração do banco ou alguma variável de ambiente estiver faltando, os comandos podem apresentar erro. Verifique a configuração da versão atual antes de prosseguir.

## 4. Como propor uma contribuição

Você pode colaborar com:

- Correções de erros de funcionamento;
- Melhorias de acessibilidade e usabilidade;
- Novas funcionalidades relacionadas a sustentabilidade e ESG;
- Testes automatizados e correção de comportamentos inesperados;
- Revisão de textos, instruções e documentação.

Antes de iniciar uma mudança grande, abra uma **Issue** no GitHub ou converse com a equipe para explicar o problema, a solução sugerida e quais partes do site serão afetadas. Isso evita retrabalho e conflitos.

## 5. Como modificar o código e enviar sua contribuição

### 5.1. Atualize seu repositório

Trabalhe sempre a partir da versão mais recente de `main`. Se você faz parte da equipe e tem acesso direto, use:

```bash
git checkout main
git pull origin main
```

Para colaboradores externos, atualize seu fork com as alterações do repositório original antes de começar (por exemplo, por meio da opção **Sync fork** no GitHub).

### 5.2. Crie uma branch para sua contribuição

Para contribuições externas, recomendamos uma branch específica:

```bash
git checkout -b melhoria/descricao-curta
```

Exemplos: `correcao/erro-login`, `melhoria/acessibilidade` ou `docs/instalacao`.

> Integrantes da equipe podem seguir o fluxo interno combinado para a branch `main`; para contribuições externas, prefira uma Pull Request.

### 5.3. Faça alterações pequenas e bem identificadas

- Siga a organização existente do projeto.
- Utilize nomes claros para funções, variáveis e arquivos.
- Evite alterar funcionalidades sem relação com a sua proposta.
- Preserve o comportamento de páginas já existentes.
- Não envie ambientes virtuais, arquivos temporários ou informações sensíveis.
- Adicione ou atualize testes quando modificar comportamentos.

### 5.4. Verifique sua alteração

Execute, quando o ambiente estiver configurado:

```bash
python manage.py check
python manage.py test
```

Teste também manualmente a página alterada e os principais fluxos relacionados. Se sua alteração envolver funcionalidades de navegador ou testes E2E, siga as instruções específicas dessa suíte no repositório, quando disponíveis.

### 5.5. Registre um commit

```bash
git status
git add caminho/do/arquivo_alterado.py
git commit -m "Descreve objetivamente a alteracao"
```

Prefira commits com mensagens claras, como `Corrige validacao do formulario` ou `Adiciona testes do detector de greenwashing`.

### 5.6. Envie uma Pull Request

Se estiver usando uma branch:

```bash
git push origin melhoria/descricao-curta
```

Depois, no GitHub, abra uma **Pull Request** direcionada à branch `main` do repositório original. Na descrição, informe:

1. O problema ou necessidade atendida;
2. O que foi alterado;
3. Como testar a mudança;
4. Capturas de tela, se houver mudança visual;
5. Issues relacionadas, se aplicável.

A equipe poderá solicitar ajustes antes de incorporar a contribuição. **Não envie diretamente para a `main` do repositório original sem autorização.**

## 6. Como relatar erros ou sugerir melhorias

Abra uma **Issue** na aba *Issues* do repositório e inclua, sempre que possível:

- **Título:** um resumo claro;
- **Descrição:** o que aconteceu ou o que poderia melhorar;
- **Passos para reproduzir:** como encontrar o problema;
- **Resultado esperado e resultado observado:** qual é a diferença;
- **Ambiente:** navegador, sistema operacional e versão, quando relevantes;
- **Captura de tela:** se ajudar a demonstrar o problema.

Não inclua senhas, dados pessoais de terceiros, tokens ou chaves de API nas Issues.

## 7. Boas práticas de colaboração

- Seja respeitoso nas discussões e revisões de código.
- Considere a acessibilidade ao criar interfaces.
- Documente decisões importantes e mantenha o README atualizado quando necessário.
- Evite dados reais ou sensíveis nos testes e exemplos.
- Espere a revisão da equipe antes de considerar uma contribuição integrada ao projeto.

## 8. Links úteis

- [Página inicial e documentação do projeto](README.md)
- [Repositório do Ecomply](https://github.com/mariaeugeniamoraes/projeto_fds_2026.2)
- [Issues — erros e sugestões](https://github.com/mariaeugeniamoraes/projeto_fds_2026.2/issues)

---

**Obrigado por contribuir com o Ecomply!** Cada melhoria ajuda a tornar a plataforma mais útil, acessível e comprometida com boas práticas de sustentabilidade.
