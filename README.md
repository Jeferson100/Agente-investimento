
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python" alt="Python 3.10+"/>
  <img src=https://img.shields.io/badge/LangChain-ffffff?logo=langchain&logoColor=green alt="LangChain"/>
  <img src="https://img.shields.io/badge/Groq-API-orange?style=flat" alt="Groq API"/>
  <img src="https://img.shields.io/badge/yFinance-Stock%20Data-green?style=flat" alt="yFinance"/>
  <img src="https://img.shields.io/badge/Finta-Technical%20Indicators-blueviolet" alt="Finta"/>
  <img src="https://img.shields.io/badge/Serper%20API-News%20Sentiment-yellow" alt="Serper API"/>
  <img src="https://img.shields.io/badge/Pandas%20-Dataframe-blue?style=flat&logo=pandas" alt="Pandas"/>
  <img src="https://img.shields.io/badge/Streamlit-Framework-red?style=flat&logo=streamlit" alt="Streamlit"/>
</p>

<h1 align="center">📈 Agente-Investimento: Seu Analista de Ações com Inteligência Artificial</h1>

<p align="center">
  O <b>Agente-Investimento</b> é uma ferramenta que integra o poder dos <b>Grandes Modelos de Linguagem (LLMs)</b> com dados do mercado financeiro brasileiro para fornecer análises de ações. Ele consolida <b>Análise Fundamentalista</b>, <b>Análise Técnica</b>, <b>Análise de Sentimento</b> e <b>Valuation</b>, tentando capacitar investidores com insights para a tomada de decisão.
</p>

<p align="center">
<a href="https://jeferson100-agente-investimen-app-streamlit1-analiseacao-lmfxza.streamlit.app/" target="_blank">
    <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Streamlit App"/>
  </a>
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

*  **Analise indicadores técnicos:**Analisa indicadores técnicos como médias móveis, RSI, MACD e Bandas de Bollinger.
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

### Pré-requisitos

*   **Chave de API Groq**: Para interação com o LLM.
*   **Chave de API Serper:** Para a Análise de Sentimento.


### Passo a Passo

1.  **Chave de API Groq:**
    *   Na primeira execução, insira a sua chave de API Groq.
    *   Ela será salva na sessão para evitar que você precise inseri-la novamente.
2.  **Selecionar Ticker:** Digite o código da ação brasileira (ex: `BBDC4`, `PETR4`, `VALE3`) no campo de busca.
3.  **Explorar as Análises:** Navegue pelas abas na barra lateral para acessar:
    *   **Análise Fundamentalista:** Mergulhe nos dados financeiros da empresa.
    *   **Análise Técnica:** Visualize os gráficos e os indicadores técnicos.
    *   **Análise de Sentimento:** Entenda a percepção do mercado sobre a ação.
    *   **Valuation:** Descubra as métricas de valuation e o potencial valor da ação.
4.  **Interagir com a IA:** Faça perguntas sobre o ticker no chat e obtenha respostas detalhadas.
5.  **Download de Dados:** Em cada página, baixe os dados em formato `.csv` ou `.md` para análise posterior.

## Estrutura de Arquivos

```bash
Agente-investimento/ 
├── app_streamlit/               # Código do Streamlit
│   ├── 1_AnaliseAcao.py                # Página inicial
│   ├── pages/                    # Páginas da aplicação
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