# 📈 Agente-investimento: Ferramenta de Análise de Investimentos Impulsionada por IA

**Agente-investimento** é um projeto que utiliza **Grandes Modelos de Linguagem (LLMs)** e diversas fontes de dados para fornecer análises abrangentes de ações do mercado brasileiro.  
A ferramenta integra **Análise Fundamentalista, Análise Técnica, Análise de Sentimento e Valuation**, gerando insights valiosos para investidores.  

## 🚀 Funcionalidades

✅ **Análise Fundamentalista:** Avaliação da saúde financeira de empresas.  
✅ **Análise Técnica:** Indicadores gráficos e tendências de mercado.  
✅ **Análise de Sentimento:** Coleta e interpretação de notícias do mercado.  
✅ **Valuation:** Estimativa do valor intrínseco de uma ação.  

## 🛠️ Tecnologias Utilizadas

- **Python** 🐍 - Linguagem principal do projeto.  
- **Streamlit** 🎨 - Framework para a interface interativa.  
- **Groq API** 🤖 - Processamento de linguagem natural com LLMs.  
- **yfinance** 📊 - Dados de ações do Yahoo Finance.  
- **finta** 📈 - Cálculo de indicadores técnicos.  
- **Serper API** 📰 - Coleta de notícias para análise de sentimento.  
- **Pandas** 📑 - Manipulação de dados.  
- **Pydantic** ✅ - Validação de dados.  

## 📥 Instalação e Configuração

1️⃣ **Clone o repositório:**  
```bash
git clone https://github.com/Jeferson100/Agente-investimento.git
cd Agente-investimento
```	

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

    *  Serao necessarias as seguintes variaveis de ambiente:

    ```properties
    GROQ_API_KEY="sua_chave_de_api_groq"
    API_KEY_SERPER="sua_chave_de_api_serper"

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

```bash
Agente-investimento/ 
├── app_streamlit/               # Código do Streamlit
│   ├── Home.py                  # Página inicial
│   ├── Pages/                    # Páginas da aplicação
│   │   ├── 1_AnaliseFundamentalista.py
│   │   ├── 2_AnaliseTecnica.py
│   │   ├── 3_AnaliseSentimento.py
│   │   └── 4_AnaliseValuation.py
│   └── __init__.py
├── coleta_dados/                 # Módulos de coleta de dados
├── chat_bots/                     # Módulos do chatbot
├── juncao_modelos_dados/          # Modelos de IA e integração de dados
├── utils/                         # Funções utilitárias
├── .gitignore                     # Arquivos ignorados pelo Git
├── requirements.txt               # Dependências do projeto
├── README.md                      # Este arquivo
└── imagem/                        # Imagens utilizadas no projeto
```

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

## 🤝 Contribuindo

Contribuições para este projeto são bem-vindas! Se você tem ideias de melhorias ou novos recursos, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## 📜 Licença

Este projeto é licenciado sob a [Licença MIT](LICENSE).

## ⚠️ Aviso Legal

<div style="background-color:#FF6347; padding: 10px; border-radius: 5px;">
<p style="color: #000000;">🚨 Aviso Importante:</p>
<p style="color: #000000;">Os resultados fornecidos por este sistema são meramente informativos e não devem ser considerados como recomendações de investimento.</p>
<p style="color: #000000;">Sempre realize sua própria análise antes de tomar qualquer decisão financeira.</p>
</div>

## 📞 Contatos

<div style="display: inline-block; margin-right: 10px;">
<a href="https://github.com/Jeferson100/Agente-investimento">
<img src="https://img.shields.io/badge/github-100000?style=for-the-badge&logo=github">
</a>
</div>
<div style="display: inline-block;">
<a href="https://www.linkedin.com/in/jefersonsehnem/">
<img src="https://img.shields.io/badge/linkedin-0077B5?style=for-the-badge&logo=linkedin&logoColor=white">
</a>
</div>