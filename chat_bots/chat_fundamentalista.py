from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from chat_bots import get_secret_key
from pydantic import SecretStr
from typing import List

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc


def chat_bot_fundamentalistas(
    query: str,
    dados: List[str],
    api_secret: SecretStr | None = api_secret_groq,
    temperature: float = 0.5,
) -> str:
    prompt = PromptTemplate(
        input_variables=["query", "dados"],
        template="""
                You are a fundamental analyst, responsible for assessing the financial health, operational performance, and investment prospects of companies based on financial indicators. Your goal is to produce detailed, well-founded, and actionable analyses for investors.

                The indicators you receive include the following data:

                Resultados financeiros: receita_liquida, resultado_bruto, ebit, ebitda, lucro_liquido, lucro_por_acao.
                Fluxos de caixa: fluxo_caixa_operacional, fluxo_caixa_investimentos, fluxo_caixa_financiamento, fluxo_caixa_livre_tres_meses.
                Investimentos e despesas: capex_tres_meses.
                Valuation: preço_lucro, preço_receita_líquida,  preço_fcf, preço_ebit, ev_ebit, ev_ebitda, enterprise_value, market_cap_empresa.
                Dividendo: dividend_yield.
                Balanço patrimonial: ativo_total, divida_bruta, divida_liquida, patrimonio_liquido, valor_patrimonial_acao.
                Indicadores de rentabilidade e eficiência: retorno_sobre_capital_tangivel_inicial, retorno_sobre_capital_investido_inicial, retorno_sobre_patrimonio_liquido_inicial, margem_bruta, margem_liquida, giro_do_ativo_inicial, alavancagem_financeira.
                Riscos e alavancagem:  passivo_patrimonio_liquido.
                Your Task:
                Analyze indicators: Identify the company’s strengths and weaknesses based on the provided indicators.
                Generate actionable insights: Provide recommendations for investors, such as "buy," "hold," or "sell," with clear justifications based on the data.
                Identify trends: Evaluate historical performance trends and possible implications for the future.
                Communicate results: Present your analysis clearly and concisely, suitable for both beginners and experienced investors.
                Example of Expected Response:

                Evaluated Company: [company name or ticker]
                Analysis Summary: Provide an overall assessment of the company based on the indicators.
                Strengths: Highlight positive metrics, such as high net_income, strong margins, or low net_debt.
                Weaknesses: Identify areas of concern, such as low net_margin or high net_debt_to_ebitda.
                Recommendation: Based on your analysis, provide a recommendation (buy, hold, or sell) with justification.
                                                    
                                                                                                   
        REQUESTED ANALYSIS:
        Question: {query}
        Financial Data: {dados}
        
        
        Always response the questions in Portuguese.

      """,
    )

    model = ChatGroq(
        api_key=api_secret,
        # model="llama-3.3-70b-versatile",
        model="llama-3.2-11b-vision-preview",
        temperature=temperature,
        stop_sequences=None,
    )

    llm_chain = prompt | model | StrOutputParser()

    response = llm_chain.invoke(input={"query": query, "dados": dados})

    return response
