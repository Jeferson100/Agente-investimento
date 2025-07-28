<p align="center">
<img src="imagem/logo_robo.png" alt="Logo Agente-Investimento" width="200"/>
</p>


<h1 align="center">📈 Agente-Investimento: Seu Analista de Ações com Inteligência Artificial</h1>

| | |
|-----------|-----------|
| **Testing**  | [![Unit Test](https://github.com/Jeferson100/Agente-investimento/actions/workflows/teste.yml/badge.svg)](https://github.com/Jeferson100/Agente-investimento/actions/workflows/teste.yml) |
| **Package**  | ![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python) ![LangChain](https://img.shields.io/badge/LangChain-ffffff?logo=langchain&logoColor=green) ![Groq](https://img.shields.io/badge/Groq-API-green?style=flat) ![yFinance](https://img.shields.io/badge/yFinance-Stock%20-green) ![Finta](https://img.shields.io/badge/Finta-blueviolet) ![Serper API](https://img.shields.io/badge/Serper%20API-yellow) ![Pandas](https://img.shields.io/badge/Pandas%20-blue?style=flat&logo=pandas) ![Streamlit](https://img.shields.io/badge/Streamlit-green?style=flat&logo=streamlit) |
| **App Streamlit** | <p align=""><a href="https://jeferson100-agente-investimen-app-streamlit1-analiseacao-lmfxza.streamlit.app/" target="_blank"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Streamlit App"/></a></p> ||
| | |


<p align="center">
  O <b>Agente-Investimento</b> é uma ferramenta que integra o poder dos <b>Grandes Modelos de Linguagem (LLMs)</b> com dados do mercado financeiro brasileiro para fornecer análises de ações. Ele consolida <b>Análise Fundamentalista</b>, <b>Análise Técnica</b>, <b>Análise de Sentimento</b> e <b>Valuation</b>, tentando capacitar investidores com insights para a tomada de decisão. 

  Ele criado com a biblioteca [LangChain](https://python.langchain.com/docs/get_started/introduction) e [LangGraph](https://github.com/langchain-ai/langgraph) tendo como fluxograma a seguinte estrutura:


 <p align="center">
<img src="laggraph_imagem.png" alt="Imagem do fluxo langgraph" width="800"/>
</p>


## ✨ Destaques do Agente-Investimento

*   **Análises Completas:** Obtenha uma visão holística do desempenho de uma ação, combinando diferentes abordagens de análise.
*   **Inteligência Artificial Avançada:** Utilize o poder dos LLMs para insights mais profundos e contextualizados.
*   **Dados Precisos:** A ferramenta integra diversas fontes de dados financeiros para garantir informações atualizadas.
*   **Interface Intuitiva:** Navegue facilmente pelas análises e interaja com a IA através de uma interfacedesenvolvida com Streamlit.
*   **Mercado Brasileiro:** Focado em ações negociadas na B3 (Bolsa de Valores Brasileira).

## 🚀 Funcionalidades

### 📊 Análise Fundamentalista

*   **Saúde Financeira:** Avaliação do desempenho financeiro da empresa, incluindo demonstrações contábeis e balanços patrimoniais.
*   **Indicadores-Chave:** Análise de indicadores essenciais como P/L (Preço/Lucro), ROE (Retorno sobre o Patrimônio Líquido), EBITDA (Lucros antes de Juros, Impostos, Depreciação e Amortização) e outros.
*   **Potencial de Crescimento:** Insights sobre a capacidade da empresa de expandir seus negócios e gerar lucros.

### 📉 Análise Técnica

*  **Analise indicadores técnicos:** Analisa indicadores técnicos como médias móveis, RSI, MACD e Bandas de Bollinger.
*   **Oportunidades de Negociação:** Identifica potenciais oportunidades de negociação com base em padrões gráficos e sinais de indicadores.
* **Tendências de Mercado:** Compreenda melhor as tendências e movimentos de preço do mercado.

### 📰 Análise de Sentimento

*   **Opinião do Mercado:** Avaliação do sentimento geral do mercado em relação à ação, baseada em notícias e artigos.
*   **Integração com Serper API:** Utilização da API Serper para agregar notícias relevantes e atuais.
*   **Pontuação de Sentimento:** Classificação do sentimento como positivo, negativo ou neutro, facilitando a compreensão do cenário.

### 💰 Valuation (Avaliação)
*   **Valor Intrínseco:** Estimativa do valor intrínseco da ação utilizando técnicas como Fluxo de Caixa Descontado (DCF) e o Modelo de Gordon.
*   **Fatores Considerados:** Análise de lucros, taxas de crescimento, comparáveis de mercado e outros fatores relevantes.
*   **Sobre/Subvalorização:** Identificação de ações que podem estar sobrevalorizadas ou subvalorizadas pelo mercado.

## ⚙️ Configurações e Uso

### 📜✔ Pré-requisitos

Antes de começar a utilizar o Agente-Investimento, você precisará obter as seguintes chaves de API:

*   **Chave de API Groq:**
    *   **Finalidade:** Essencial para interagir com o Grande Modelo de Linguagem (LLM) e obter respostas detalhadas e contextualizadas nas análises e no chatbot.
    *   **Obtenção:**
        1.  Acesse o site da [![Groq API](https://img.shields.io/badge/Create%20Groq%20API%20Key-black?style=flat&logo=groq)](https://console.groq.com/keys) e crie uma conta.
        2.  Após o cadastro, vá para a seção de API Keys e gere uma nova chave.
        3.  Copie e guarde a chave gerada, pois ela será necessária para configurar o aplicativo.
    *   **Utilização**: A chave deve ser inserida na primeira execução do aplicativo, no local indicado.

*   **Chave de API Serper:**
    *   **Finalidade:** Necessária para realizar a Análise de Sentimento, permitindo a busca e análise de notícias relevantes sobre as ações.
    *   **Obtenção:**
        1.  Acesse o site da [![Groq API](https://img.shields.io/badge/Create%20Serper%20API%20Key-blue?style=flat&logo=groq)](https://serper.dev/api-key) e crie uma conta.
        2.  Após o cadastro, vá para a seção de API Keys (ou similar) e gere uma nova chave.
        3.  Copie e guarde a chave gerada para configurar o aplicativo.
    * **Importante:** Esse modelo utiliza a API Gratuita da Serper, então tem um limite de Requisições mensais.

## 🚀 Executando o Bot

### 🐳 Executando com Docker

O Agente-Investimento pode ser executado em um container Docker, permitindo uma execução simples e consistente.

```bash 
docker build -t agente-investimento-app .
docker run -p 3000:3000 agente-investimento-app

docker-compose build
docker-compose up
```

### 🚀 Executando com Streamlit

O Agente-Investimento pode ser utilizado com o Streamlit, atraves do seguinte link:

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

Tambem pode ser executado localmente, utilizando o seguinte comando:

```bash
pip install -r requirements.txt
streamlit run app/app_streamlit.py
```

### Executando com o chainlit

O Agente-Investimento pode ser utilizado com o chainlit, atraves do seguinte comando:

```bash
pip install -r requirements.txt
chainlit run app/app_chainlit.py
```

## 📂 Estrutura do Projeto

A estrutura de diretórios do projeto está organizada da seguinte forma:

```bash
Agente-investimento/
├── app/                      # Código das aplicações (Streamlit, Chainlit)
├── agente_investimento/      # Core do agente e lógica de análise
│   ├── chat_bots/            # Módulos do chatbot
│   ├── coleta_dados/         # Módulos de coleta de dados
│   ├── juncao_modelos_dados/ # Modelos de IA e integração de dados
│   ├── tratando_dados/       # Scripts para tratamento e limpeza de dados
│   └── utils/                # Funções utilitárias
├── imagem/                   # Imagens utilizadas no projeto
├── testes/                   # Testes unitários e de integração
├── .env.example              # Arquivo de exemplo para variáveis de ambiente
├── .gitignore                # Arquivos ignorados pelo Git
├── docker-compose.yml        # Configuração do Docker Compose
├── Dockerfile                # Configuração do container Docker
├── requirements.txt          # Dependências do projeto
└── README.md                 # Este arquivo
```

*   `Agente-investimento/`: Diretório raiz do projeto.
* `app/`: Contém os scripts de inicialização das interfaces web (`app_streamlit.py`, `app_chainlit.py`).
*   `coleta_dados/`: Módulos responsáveis pela coleta dos dados externos de diversas fontes.
    *   `fundamentos/`: Diretório que contém os módulos responsáveis por cálculos e análises relacionados aos fundamentos das empresas.
        *   `calculo_wacc.py`: Módulo que implementa o cálculo do WACC (Custo Médio Ponderado de Capital), uma métrica fundamental para a avaliação financeira de empresas.
        *   `indicadores_financeiros.py`: Módulo que calcula diversos indicadores financeiros, como liquidez, rentabilidade, endividamento, entre outros, que são essenciais para a Análise Fundamentalista.
        *   `necessidade_capital_giro.py`: Módulo que calcula a Necessidade de Capital de Giro (NCG), um indicador importante para entender a capacidade da empresa de financiar suas operações de curto prazo.
        *   `outros_ativos_nao_operecionais.py`: Módulo que trata da identificação e análise de outros ativos não operacionais, auxiliando na determinação do valor real da empresa.
        *   `passivos_menos_divida.py`: Módulo que calcula o valor dos passivos da empresa menos a dívida, sendo um passo importante na análise do endividamento e saúde financeira.
        *   `valuation_fluxo_caixa_descontado.py`: Módulo que implementa o método de Valuation (Avaliação) por Fluxo de Caixa Descontado (DCF), usado para estimar o valor intrínseco de uma empresa.
        *   `valuation_metodo_gordon.py`: Módulo que implementa o método de Valuation (Avaliação) de Gordon, utilizado para estimar o valor intrínseco de uma empresa com base em dividendos futuros.
        *   `variacao_receita.py`: Módulo que calcula a variação da receita da empresa, analisando o seu crescimento ou declínio ao longo do tempo.
    *   `dados_fundamentalistas.py`: Módulo responsável pela coleta de dados fundamentalistas de empresas, como balanços patrimoniais, demonstrativos de resultados e outros indicadores financeiros.
    *   `dados_indicadores_tecnicos.py`: Módulo responsável pela coleta de indicadores técnicos, que podem ser usados na Análise Técnica, como médias móveis, RSI, MACD, etc.
    *   `dados_noticias_google.py`: Módulo responsável por coletar notícias sobre ações, utilizando o Google News como fonte.
    *   `dados_noticias_yahoo.py`: Módulo responsável por coletar notícias sobre ações, utilizando o Yahoo Search como fonte. Extrai links, títulos, fontes e datas das notícias.
    *   `dados_text_html.py`: Módulo responsável por processar ou extrair dados de arquivos HTML, possivelmente para obter informações financeiras ou de notícias.
    *   `verificador_ticks.py`: Módulo responsável por verificar a validade ou existência de tickers de ações, provavelmente para assegurar que os dados sejam coletados apenas para ações válidas.

*   `chat_bots/`: Módulo que contém os arquivos responsáveis pela implementação da lógica e da interface do chatbot, permitindo a interação do usuário com a IA do sistema por meio de perguntas e respostas sobre as análises.
    *   `chat_analise_tecnica.py`: Módulo que implementa a lógica do chatbot para interagir com o usuário sobre Análise Técnica de ações, respondendo a perguntas e fornecendo informações relacionadas a esse tipo de análise.
    *   `chat_bots.py`: Módulo central do chatbot, provavelmente contém a classe principal ou funções que controlam o fluxo geral da conversa e a interação com o usuário.
    *   `chat_fundamentalista.py`: Módulo que implementa a lógica do chatbot para interagir com o usuário sobre Análise Fundamentalista de ações, respondendo a perguntas e fornecendo informações relacionadas a esse tipo de análise.
    *   `chat_limpa_resposta.py`: Módulo que contém funções para processar e formatar as informações fornecidas ao LLM, removendo informações desnecessárias e melhorando a legibilidade.
    *   `chat_sentimentalista.py`: Módulo que implementa a lógica do chatbot para interagir com o usuário sobre Análise de Sentimento de ações, respondendo a perguntas e fornecendo informações relacionadas a esse tipo de análise.
    *   `chat_tradutor.py`: Módulo que implementa funções para traduzir textos do inglês para o português.
    *   `chat_valuation.py`: Módulo que implementa a lógica do chatbot para interagir com o usuário sobre Valuation (Avaliação) de ações, respondendo a perguntas e fornecendo informações relacionadas a esse tipo de análise.
    *   `verificacao_key.py`: Módulo que contém a lógica para verificar a validade das chaves de API necessárias para o funcionamento do chatbot e outras funcionalidades.

*   `juncao_modelos_dados/`: Módulo que contém os arquivos responsáveis pela integração dos Modelos de Linguagem (LLMs) com os dados coletados e o processamento para a geração de análises.
    *   `modelo_analise_tecnica.py`: Módulo que implementa o modelo de Inteligência Artificial (IA) para realizar a Análise Técnica de ações, integrando os dados de indicadores técnicos e gerando insights.
    *   `modelo_fundamentos.py`: Módulo que implementa o modelo de Inteligência Artificial (IA) para realizar a Análise Fundamentalista de ações, integrando os dados financeiros e gerando insights.
    *   `modelo_sentimento.py`: Módulo que implementa o modelo de Inteligência Artificial (IA) para realizar a Análise de Sentimento de notícias sobre ações, integrando os dados coletados e gerando insights.
    *   `modelo_valuation.py`: Módulo que implementa o modelo de Inteligência Artificial (IA) para realizar o Valuation (Avaliação) de ações, integrando os dados financeiros e gerando insights.

* `langraph_construcao/`: Módulo que contém os arquivos responsáveis pela criação e gerenciamento de gráficos e arquivos de dados para o sistema LangGraph.
    *   `chat_bot_padrao.py`: Módulo que implementa o chatbot padrão do sistema LangGraph, que responde perguntas que foram respondidas pelo chatbot principal.
    *   `chat_bot_response.py`: Módulo que contém chat bots que respondem perguntas relacionadas aos investimentos.
    *   `identifica_metodo_analise.py`: Módulo que tenta identificar o tipo de análise que deve ser feita com base nas perguntas do usuário.
    *   `identifica_ticks.py`: Módulo que tenta identificar os tickers de ações que foram mencionados nas perguntas do usuário.
    *   `langgraph_main.py`: Módulo principal do sistema LangGraph, que coordena a criação e gerenciamento de gráficos e arquivos de dados.
    *   `supervisor_node.py`: Módulo que supervisiona qual método de análise deve ser executado a seguir.
    *   `type_state.py`: Módulo que contém a classe State, que representa o estado do sistema LangGraph e suas transições.
    *   `verifica_tick.py`: Módulo que verifica se os tickers de ações mencionados nas perguntas do usuário são válidos.

*   `tratando_dados/`: Módulo que contém os arquivos responsáveis pelo tratamento, limpeza e preparação dos dados coletados, deixando-os em um formato adequado para serem utilizados pelos modelos de análise e pelo chatbot.
    *   `tratando_dados_indicadores.py`: Módulo responsável por tratar e formatar os dados de indicadores técnicos, preparando-os para serem utilizados nas análises técnicas.
    *   `tratando_dados_valuation.py`: Módulo responsável por tratar e formatar os dados financeiros, preparando-os para serem utilizados nos modelos de Valuation.
    *   `tratar_dados_fundamentalistas.py`: Módulo responsável por tratar e formatar os dados fundamentalistas das empresas, preparando-os para serem utilizados nas análises fundamentalistas.
    *   `tratar_dados_noticias.py`: Módulo responsável por tratar e formatar os dados de notícias, preparando-os para serem utilizados na análise de sentimento.
*   `utils/`: Módulo que contém funções utilitárias, classes e códigos reutilizáveis que auxiliam em diversas tarefas dentro do projeto.
    *   `funcoes_utils.py`: Módulo que contém funções utilitárias gerais que são utilizadas por outros módulos do projeto, como por exemplo: tratamento de texto, formatações, conversões, etc.
    *   `pegando_logo_marca.py`: Módulo que contém classes ou funções para obter o logotipo de uma empresa a partir de uma fonte externa, como um site financeiro.
*   `.gitignore`: Arquivo que especifica os arquivos e pastas que o Git deve ignorar, como arquivos temporários ou confidenciais.
*   `requirements.txt`: Lista das dependências do projeto, especificando os pacotes Python e suas versões.
*   `README.md`: Arquivo de documentação principal do projeto, fornecendo informações sobre o objetivo, uso e estrutura do projeto.



## 🤝 Contribuindo

Contribuições para este projeto são bem-vindas! Se você tem ideias de melhorias ou novos recursos, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## 📜 Licença

Este projeto é licenciado sob a [Licença MIT](LICENSE).

## ⚠️ **AVISO LEGAL** ⚠️

🚨 **ATENÇÃO:** Os resultados fornecidos por este sistema são **meramente informativos** e **não** devem ser considerados como recomendações de investimento.  
📌 Sempre realize sua **própria análise** antes de tomar qualquer decisão financeira.

## 📞 Contatos

| GitHub | LinkedIn |
|--------|---------|
| [![GitHub](https://img.shields.io/badge/github-100000?style=for-the-badge&logo=github)](https://github.com/Jeferson100/Agente-investimento) | [![LinkedIn](https://img.shields.io/badge/linkedin-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jefersonsehnem/) |
