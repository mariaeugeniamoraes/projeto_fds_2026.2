# Histórias de Usuário — Ecomply

## 1. Sobre as histórias

O Ecomply é uma plataforma voltada para pequenas e médias empresas de e-commerce que desejam acompanhar e melhorar seu desempenho ambiental, social e de governança (ESG).

Este documento descreve as histórias de usuário do projeto, seus critérios de aceitação e os cenários de validação utilizando BDD (Behavior-Driven Development).

## 2. Histórias de usuário

### HU01 — Calculadora de Embalagens Sustentáveis

**Como** lojista de um e-commerce,  
**quero** comparar diferentes materiais de embalagem,  
**para** identificar alternativas que reduzam os custos e o impacto ambiental do meu negócio.

**Critérios de aceitação**
- O usuário deve conseguir informar os dados necessários para comparar as embalagens.
- O sistema deve validar os campos obrigatórios e os valores informados.
- O sistema deve apresentar os resultados da comparação entre as alternativas disponíveis.
- Os resultados devem ser apresentados de forma clara para auxiliar a tomada de decisão.

**Cenários BDD**

**Cenário 1: Comparação de embalagens com dados válidos**

Dado que o lojista acessou a calculadora de embalagens sustentáveis  
E informou os dados necessários para a comparação  
Quando solicitar a comparação das alternativas  
Então o sistema deve apresentar os resultados calculados para as opções disponíveis.

**Cenário 2: Tentativa de comparação com dados inválidos**

Dado que o lojista acessou a calculadora  
E informou dados inválidos ou deixou campos obrigatórios vazios  
Quando solicitar a comparação  
Então o sistema deve informar quais dados precisam ser corrigidos.

### HU02 — Gerador de Plano ESG

**Como** responsável por uma pequena empresa de e-commerce,  
**quero** responder a perguntas sobre meu negócio,  
**para** receber sugestões de ações que contribuam para melhorar meu desempenho ESG.

**Critérios de aceitação**
- O sistema deve apresentar perguntas relacionadas às práticas ESG da empresa.
- O usuário deve conseguir responder às perguntas apresentadas.
- O sistema deve gerar sugestões de ações com base nas respostas fornecidas.
- O resultado deve ser apresentado de maneira organizada e compreensível.

**Cenários BDD**

**Cenário 1: Geração de plano com respostas válidas**

Dado que o usuário iniciou o preenchimento do questionário ESG  
E respondeu às perguntas obrigatórias  
Quando solicitar a geração do plano  
Então o sistema deve apresentar sugestões de ações relacionadas às respostas fornecidas.

**Cenário 2: Questionário incompleto**

Dado que o usuário iniciou o preenchimento do questionário  
E deixou perguntas obrigatórias sem resposta  
Quando tentar gerar o plano  
Então o sistema deve informar que o preenchimento precisa ser concluído.

### HU03 — Painel de Controle ESG do Lojista

**Como** lojista de um e-commerce,  
**quero** visualizar informações sobre o desempenho ESG da minha empresa,  
**para** acompanhar seus indicadores e identificar oportunidades de melhoria.

**Critérios de aceitação**
- O painel deve apresentar os indicadores disponíveis para a empresa.
- As informações devem estar organizadas de forma clara.
- Os dados exibidos devem corresponder à empresa selecionada pelo usuário.
- O sistema deve apresentar uma mensagem apropriada quando não houver dados disponíveis.

**Cenários BDD**

**Cenário 1: Visualização dos indicadores**

Dado que o usuário possui uma empresa cadastrada  
E existem indicadores ESG registrados para essa empresa  
Quando acessar o painel de controle  
Então o sistema deve apresentar os indicadores correspondentes à empresa.

**Cenário 2: Ausência de indicadores**

Dado que o usuário acessou o painel de controle  
E não existem indicadores registrados para a empresa  
Quando a página for carregada  
Então o sistema deve informar que não há dados disponíveis para exibição.

### HU04 — Geração de Planilhas e Gráficos

**Como** lojista,  
**quero** visualizar e exportar informações sobre os custos e resultados do meu negócio,  
**para** analisar os dados e apoiar minhas decisões financeiras e ambientais.

**Critérios de aceitação**
- O sistema deve permitir a visualização das informações disponíveis.
- Os gráficos devem representar os dados utilizados na análise.
- Quando a exportação estiver disponível, o sistema deve gerar uma planilha com os dados selecionados.
- O sistema deve informar quando não houver dados suficientes para gerar a visualização solicitada.

**Cenários BDD**

**Cenário 1: Visualização de dados disponíveis**

Dado que existem dados registrados para a análise  
Quando o usuário acessar a seção de gráficos  
Então o sistema deve apresentar uma visualização compatível com os dados disponíveis.

**Cenário 2: Tentativa de gerar relatório sem dados**

Dado que não existem dados suficientes para a análise  
Quando o usuário solicitar um gráfico ou relatório  
Então o sistema deve informar que não há dados suficientes para gerar o resultado.

### HU05 — Portal da Transparência ESG

**Como** consumidor ou visitante do site,  
**quero** consultar informações públicas sobre as práticas ESG de uma empresa,  
**para** conhecer suas iniciativas e avaliar seu compromisso com a sustentabilidade.

**Critérios de aceitação**
- O portal deve apresentar as informações públicas disponibilizadas pela empresa.
- Os dados devem ser organizados de maneira compreensível.
- As informações públicas não devem expor dados privados de usuários.
- O sistema deve informar quando a empresa não possuir informações públicas cadastradas.

**Cenários BDD**

**Cenário 1: Consulta às informações públicas**

Dado que uma empresa disponibilizou informações ESG para consulta pública  
Quando um visitante acessar o portal da empresa  
Então o sistema deve apresentar as informações públicas cadastradas.

**Cenário 2: Empresa sem informações públicas**

Dado que o visitante acessou o portal de uma empresa  
E não existem informações públicas cadastradas  
Quando a página for carregada  
Então o sistema deve informar que não há informações disponíveis.

### HU06 — Acessibilidade da Plataforma

**Como** usuário do Ecomply com necessidades de acessibilidade,  
**quero** utilizar recursos que facilitem a leitura e a navegação,  
**para** acessar as funcionalidades da plataforma de maneira mais confortável e inclusiva.

**Critérios de aceitação**
- Os recursos de acessibilidade disponibilizados devem poder ser ativados pelo usuário.
- A interface deve apresentar as alterações visuais correspondentes ao recurso selecionado.
- O usuário deve conseguir retornar à apresentação padrão.
- Os recursos devem manter os textos e as funcionalidades principais acessíveis.

**Cenários BDD**

**Cenário 1: Ativação de recurso de acessibilidade**

Dado que o usuário acessou a plataforma  
Quando ativar um recurso de acessibilidade disponível  
Então o sistema deve aplicar a alteração correspondente à interface.

**Cenário 2: Retorno à apresentação padrão**

Dado que um recurso de acessibilidade está ativo  
Quando o usuário desativá-lo  
Então o sistema deve restaurar a apresentação padrão correspondente.

## 3. Histórias selecionadas para implementação na Entrega 03

As histórias selecionadas pelo grupo para desenvolvimento nesta entrega são:

- **HU01 — Calculadora de Embalagens Sustentáveis**
- **HU02 — Gerador de Plano ESG**
- **HU03 — Painel de Controle ESG do Lojista**

A implementação de cada história deverá ser acompanhada de testes e validação dos critérios de aceitação descritos neste documento.

## 4. Observação sobre o desenvolvimento

As histórias descrevem comportamentos esperados do sistema. Sua documentação não significa que todas as funcionalidades já estejam implementadas.

O status de cada história deverá ser atualizado conforme o desenvolvimento e a validação realizados pela equipe.
