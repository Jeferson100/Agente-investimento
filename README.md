# Agente-investimento: Ferramenta de Análise de Investimentos Impulsionada por IA



**Agente-investimento** é um projeto inovador que aproveita o poder dos Grandes Modelos de Linguagem (LLMs) e diversas fontes de dados para fornecer análises abrangentes de ações para o mercado brasileiro. Esta ferramenta integra análise fundamentalista, análise técnica, análise de sentimento e valuation, oferecendo insights valiosos para investidores.

## Funcionalidades

-   **Análise Fundamentalista:** Obtenha análises aprofundadas sobre a saúde financeira de uma empresa, seu modelo de negócios e sua posição competitiva.
-   **Análise Técnica:** Analise gráficos de preços de ações e indicadores técnicos para identificar tendências e potenciais oportunidades de negociação.
-   **Análise de Sentimento:** Avalie o sentimento do mercado em relação a uma ação analisando artigos de notícias.
-   **Valuation:** Avalie o valor intrínseco de uma ação utilizando diversas técnicas de valuation.

## Tecnologias Utilizadas

-   **Python:** A linguagem de programação principal para todo o projeto.
-   **Streamlit:** Um framework para criar aplicações web interativas.
-   **Grandes Modelos de Linguagem (LLMs):** A API Groq é utilizada para obter as respostas.
-   **yfinance:** Uma biblioteca para recuperar dados de ações do Yahoo Finance.
-   **finta:** Uma biblioteca para calcular indicadores de análise técnica.
-   **Groq API:** Uma API de alto desempenho para inferência de modelos LLM.
-   **Serper API:** Para coletar notícias e informações para análise de sentimento.
-   **Pandas:** Para manipulação e análise de dados.
-   **Pydantic**: biblioteca para validação de dados.

## Instalação e Configuração

1.  **Clone o Repositório:**

    ```bash
    git clone https://github.com/Jeferson100/Agente-investimento.git
    cd Agente-investimento
    ```

2.  **Crie um Ambiente Virtual (Recomendado):**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # Em Linux/macOS
    .venv\Scripts\activate  # Em Windows
    ```

3.  **Instale as Dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Variáveis de Ambiente:**

    *   Crie um arquivo `.env` na raiz do projeto.
    *   Adicione as seguintes chaves de API e tokens ao arquivo `.env` (substitua pelos seus dados reais):

    ```properties
    GROQ_API_KEY="sua_chave_de_api_groq"
    API_KEY_SERPER="sua_chave_de_api_serper"
    LANGCHAIN_API_KEY="sua_chave_de_api_langsmith" #opcional
    TAVILY_API_KEY="sua_chave_de_api_tavily" #opcional
    FIRECRAWL_API_KEY="sua_chave_de_api_firecrawl" #opcional
    SEARCHAPI_API_KEY="sua_chave_de_api_searchapi" #opcional
    TOKIN_BRAPI="seu_token_brapi" #opcional
    ACCESS_TOKEN_TWITTER="seu_token_de_acesso_twitter" #opcional
    ACCESS_TOKEN_SECRET_TWITTER="seu_token_de_acesso_secreto_twitter" #opcional
    API_KEY_TWITTER="sua_chave_de_api_twitter" #opcional
    API_KEY_SECRET_TWITTER="sua_chave_secreta_de_api_twitter" #opcional
    BEARER_TOKEN_TWITTER="seu_bearer_token_twitter" #opcional
    LANGCHAIN_TRACING_V2= true #opcional
    LANGCHAIN_ENDPOINT="https://api.smith.langchain.com" #opcional
    LANGCHAIN_PROJECT="Bot investimentos" #opcional
    ```

    *   Certifique-se de criar o arquivo `.env` e preencher as chaves de API necessárias.
    * Você deve criar uma conta Groq, uma conta Serper e outras se quiser usar.
    * Você pode criar uma conta no Langsmith se quiser rastrear os aplicativos.

5.  **Execute o Aplicativo Streamlit:**

    ```bash
    streamlit run app_streamlit/Home.py
    ```

    *   Isso iniciará o aplicativo no seu navegador web padrão.

## Uso

1.  **Chave de API Groq:**
    -   Na primeira vez que você executar o aplicativo, deverá inserir a API Groq.
    -   Você não precisará inserir novamente, pois o aplicativo a salvará em sua sessão.
2.  **Selecione um Ticker:** Digite um código de negociação de ação brasileira (por exemplo, `BBDC4`, `PETR4`) na entrada de chat.
3.  **Explore as Análises:** Navegue pelas diferentes páginas de análise na barra lateral:
    -   **Análise Fundamentalista:** Obtenha uma análise abrangente da saúde financeira da empresa.
    -   **Análise Técnica:** Visualize gráficos e indicadores técnicos.
    -   **Análise de Sentimento:** Entenda o sentimento do mercado em relação à ação.
    -   **Valuation:** Explore métricas e avaliações de valuation.
4. **Interação com o Chat**: Você pode ter uma conversa com a IA, fazendo perguntas sobre o ticker.
5. **Download dos dados**: Em cada página, você pode baixar os dados em formato `.csv` ou `.md`.

## Estrutura de Arquivos

Agente-investimento/ 
├── app_streamlit/ # Código do aplicativo Streamlit │ ├── Home.py # Página inicial do aplicativo │ ├── Pages/ # Código para as diferentes páginas de análise │ │ ├── 1_AnaliseFundamentalista.py │ │ ├── 2_AnaliseTecnica.py │ │ ├── 3_AnaliseSentimento.py │ │ └── 4_AnaliseValuation.py │ └── init.py ├── coleta_dados/ # Módulos de coleta de dados │ ├── dados_acoes.py │ ├── dados_balanco.py │ ├── dados_dre.py │ ├── dados_fundamentalistas.py │ ├── dados_indicadores_tecnicos.py │ └── init.py ├── chat_bots/ # Lógica do chatbot │ ├── ChatBot.py │ ├── ChatTradutor.py │ └── init.py ├── juncao_modelos_dados/ # Integração de modelos e dados │ ├── ModeloAnaliseTecnica.py │ ├── ModeloFundamentos.py │ ├── ModeloSentimento.py │ ├── ModeloValuation.py │ └── init.py ├── utils/ # Funções utilitárias │ ├── init.py │ ├── pegar_logotipo.py │ ├── tratamento_dados.py │ ├── tratamento_string.py │ └── verificador_ticks.py ├── .env # Variáveis de ambiente (chaves de API) ├── .gitignore # Arquivo de ignorados do Git ├── requirements.txt # Dependências do projeto ├── README.md # Este arquivo └── imagem/ #imagens

## Páginas do Aplicativo

1.  **Análise Fundamentalista:**
    -   Fornece uma análise detalhada do desempenho financeiro da empresa.
    -   Avalia métricas-chave como receita, lucros, dívida e fluxo de caixa.
    -   Oferece insights sobre o modelo de negócios da empresa e sua posição na indústria.
2.  **Análise Técnica:**
    -   Analisa gráficos de preços de ações e indicadores técnicos como médias móveis, RSI, MACD e Bandas de Bollinger.
    -   Identifica potenciais oportunidades de negociação com base em padrões gráficos e sinais de indicadores.
    -   Ajuda na compreensão das tendências do mercado e movimentos de preços.
3.  **Análise de Sentimento:**
    -   Avalia o sentimento do mercado em relação a uma ação analisando artigos de notícias e mídias sociais.
    -   Usa a API Serper para obter informações relacionadas a notícias.
    -   Fornece uma pontuação geral de sentimento (positivo, negativo, neutro).
4.  **Valuation:**
    -   Emprega técnicas de valuation para estimar o valor intrínseco de uma ação.
    -   Considera fatores como lucros, taxas de crescimento e comparáveis de mercado.
    -   Auxilia na identificação de ações potencialmente sobrevalorizadas ou subvalorizadas.

## Contribuindo

Contribuições para este projeto são bem-vindas! Se você tem ideias de melhorias ou novos recursos, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto é licenciado sob a [Licença MIT](LICENSE).

## Aviso Legal

Esta ferramenta é apenas para fins informativos e não deve ser considerada como aconselhamento financeiro. Sempre realize sua própria pesquisa e consulte um consultor financeiro qualificado antes de tomar qualquer decisão de investimento.

## Contato

- [Jeferson Sehnem](https://www.linkedin.com/in/jefersonsehnem/)
- [Repositório GitHub](https://github.com/Jeferson100/Agente-investimento)