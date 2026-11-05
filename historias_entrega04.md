# Histórias de Usuário — Ecomply

## 1. Sobre as histórias

O Ecomply é uma plataforma voltada para pequenas e médias empresas de e-commerce que desejam acompanhar e melhorar suas práticas ambientais, sociais e de governança (ESG).

Este documento reúne as **três histórias de usuário da Entrega 04**, seus critérios de aceitação e cenários de validação utilizando **BDD (Behavior-Driven Development)**.

## 2. Histórias de usuário — Entrega 04

### HU01 — Detector de Greenwashing

**Como** gestor de uma pequena ou média empresa de e-commerce,  
**quero** analisar textos de descrições de produtos e propagandas para identificar alegações ambientais que merecem verificação,  
**para** melhorar a transparência da comunicação ambiental da minha empresa.

**Critérios de aceitação**

- O usuário autenticado deve conseguir acessar o Detector de Greenwashing pela página **Ferramentas**.
- O usuário deve conseguir inserir um texto para análise.
- O sistema deve validar a entrada, exigindo de 10 a 5.000 caracteres.
- O sistema deve identificar expressões ambientais monitoradas, como alegações absolutas ou genéricas, e apresentar os trechos encontrados.
- Para cada trecho identificado, o sistema deve exibir uma explicação e uma sugestão de melhoria.
- Após a análise, o usuário deve visualizar uma mensagem de conclusão e ser direcionado à seção de resultados.
- Quando nenhum termo monitorado for encontrado, o sistema não deve afirmar que o texto está livre de greenwashing.

**Cenários de validação (BDD)**

**Cenário 1 — Identificação de possíveis alegações problemáticas**

```gherkin
Dado que o gestor está autenticado e acessou o Detector de Greenwashing
Quando inserir "Nosso produto é 100% ecológico e totalmente sustentável"
E solicitar a análise
Então o sistema deve identificar as duas expressões monitoradas
E exibir explicações e sugestões de melhoria para cada uma
E mostrar que a análise foi concluída
```

**Cenário 2 — Texto sem expressões monitoradas**

```gherkin
Dado que o gestor acessou o Detector de Greenwashing
Quando inserir uma descrição sem expressões ambientais monitoradas
E solicitar a análise
Então o sistema deve informar que não encontrou expressões monitoradas
E esclarecer que isso não garante a ausência de greenwashing
```

**Cenário 3 — Texto inválido**

```gherkin
Dado que o gestor acessou o Detector de Greenwashing
Quando enviar um texto com menos de 10 caracteres
Então o sistema deve exibir uma mensagem de validação
E não deve gerar um resultado de análise
```

---

### HU02 — Passaporte Digital de Sustentabilidade

**Como** gestor de uma pequena ou média empresa de e-commerce,  
**quero** cadastrar informações de sustentabilidade dos meus produtos e disponibilizá-las em um passaporte digital acessível por QR Code,  
**para** oferecer mais transparência aos consumidores sobre os produtos comercializados.

**Critérios de aceitação**

- O gestor deve conseguir acessar a funcionalidade **Passaporte Digital de Sustentabilidade** pela página Ferramentas.
- O gestor deve conseguir cadastrar um passaporte associado à sua empresa, preenchendo as informações solicitadas pelo formulário.
- O sistema deve registrar os dados do passaporte para posterior consulta.
- O sistema deve disponibilizar uma página pública para visualização das informações do produto.
- O sistema deve permitir acessar o passaporte por meio de um QR Code associado a ele.
- O gestor deve conseguir visualizar os passaportes cadastrados.

**Cenários de validação (BDD)**

**Cenário 1 — Cadastro de passaporte digital**

```gherkin
Dado que o gestor está autenticado e possui uma empresa cadastrada
Quando acessar o cadastro de passaporte digital
E preencher os campos obrigatórios com dados válidos
E confirmar o cadastro
Então o sistema deve salvar o passaporte associado à empresa
E disponibilizá-lo na relação de passaportes cadastrados
```

**Cenário 2 — Consulta pública por QR Code**

```gherkin
Dado que existe um passaporte digital cadastrado
Quando um consumidor acessar o endereço vinculado ao QR Code
Então o sistema deve exibir a página pública do passaporte
E apresentar as informações de sustentabilidade cadastradas para o produto
```

---

### HU03 — Exportação do Dashboard em PDF

**Como** gestor de uma pequena ou média empresa,  
**quero** exportar as informações exibidas no dashboard em um arquivo PDF,  
**para** consultar, arquivar e compartilhar esses dados sem precisar acessar o sistema.

**Critérios de aceitação**

- O usuário autorizado deve conseguir acessar o dashboard da empresa.
- O dashboard deve oferecer uma opção de **exportação em PDF**.
- Ao solicitar a exportação, o sistema deve disponibilizar um arquivo PDF para download.
- O documento deve apresentar de forma legível as informações e os indicadores previstos na exportação.
- A exportação deve preservar o contexto da empresa correspondente, sem incluir dados de empresas às quais o usuário não tenha acesso.

**Cenários de validação (BDD)**

**Cenário 1 — Exportação do dashboard**

```gherkin
Dado que o gestor está autenticado e acessou o dashboard de sua empresa
Quando selecionar a opção de exportar em PDF
Então o sistema deve disponibilizar um arquivo no formato PDF
E o documento deve apresentar as informações previstas para exportação
```

**Cenário 2 — Restrição de acesso**

```gherkin
Dado que um usuário não possui permissão para consultar os dados de uma empresa
Quando tentar acessar a exportação do dashboard dessa empresa
Então o sistema deve impedir o acesso aos dados não autorizados
```

---

## 3. Observações sobre a validação

Os cenários acima descrevem **comportamentos esperados** para orientar testes e documentação. Eles não substituem a execução dos testes automatizados nem comprovam, por si só, que todos os critérios foram implementados. Antes da entrega, a equipe deve conferir os itens especialmente relacionados à exportação de PDF, ao controle de acesso e ao conteúdo público do passaporte.
