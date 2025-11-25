from typing import Iterator

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import SecretStr

from .chat_groq import get_llm


def ChatValuation(
    query: str,
    precos_atual_valuations: str,
    indicadores_valuation_fluxo: str,
    valuation_metodo_gordon: str,
    valuation_fluxo_caixa: str,
    api_secret: SecretStr | None,
    temperature: float = 0.5,
    modelo_llm: str = "llama-3.3-70b-versatile",
    stream: bool = False,
) -> str | Iterator[str]:
    prompt = PromptTemplate(
        input_variables=[
            "query",
            "precos_atual_valuations",
            "indicadores_valuation_fluxo",
            "valuation_metodo_gordon",
            "valuation_fluxo_caixa",
        ],
        template="""
       You are a specialized valuation agent responsible for determining if a company is undervalued or overvalued. You receive two valuation estimates and the current stock price:

        1. Gordon Growth Model (based on sustainable dividend growth):
        - Data includes median dividend, risk-free rate, beta, CAPM, sustainable growth, and estimated stock price.

        2. Discounted Cash Flow (DCF) Model:
        - Data includes annual revenue, EBIT, tax, CAPEX, depreciation, cash flow, and calculated present value of future cash flows.
        - Additional inputs: EBIT margin, revenue variation, depreciation-to-CAPEX ratio, CAPEX-to-revenue ratio, WACC, shares, total debt, available cash, assets, liabilities, and working capital.

        Your tasks:
        1. Comparison:
        - Compare the Gordon Growth valuation with the DCF valuation. Explain any significant discrepancies and the possible influencing factors.
        2. Profitability & Sustainability:
        - Assess if the company generates positive cash flow, if high CAPEX may jeopardize future cash flow, and if value generation justifies the valuation.
        3. Risks & Inconsistencies:
        - Evaluate sustainability of revenue/EBIT growth, debt levels, debt-to-cash ratio, and the appropriateness of the WACC.
        4. Conclusion & Recommendation:
        - State if the company is undervalued or overvalued and provide a clear recommendation for investors.

        REQUESTED ANALYSIS:
        Question: {query}
        Stock and Valuations: {precos_atual_valuations}
        DCF Calculation Inputs: {indicadores_valuation_fluxo}
        DCF Valuation: {valuation_fluxo_caixa}
        Gordon Growth Valuation: {valuation_metodo_gordon}

        Always respond in Portuguese. Put 'Valuation Analysis' at the beginning of the answer. Keep your answer concise and include your confidence level.
        """,
    )

    model = get_llm(
        api_groq=api_secret,
        model=modelo_llm,
        # model="llama-3.2-11b-vision-preview",
        temperature=temperature,
        stop_sequences=None,
    )

    llm_chain = prompt | model | StrOutputParser()

    if stream:
        response_stream = llm_chain.stream(
            input={
                "query": query,
                "precos_atual_valuations": precos_atual_valuations,
                "indicadores_valuation_fluxo": indicadores_valuation_fluxo,
                "valuation_metodo_gordon": valuation_metodo_gordon,
                "valuation_fluxo_caixa": valuation_fluxo_caixa,
            },
        )
        return response_stream

    else:
        response_invoke = llm_chain.invoke(
            input={
                "query": query,
                "precos_atual_valuations": precos_atual_valuations,
                "indicadores_valuation_fluxo": indicadores_valuation_fluxo,
                "valuation_metodo_gordon": valuation_metodo_gordon,
                "valuation_fluxo_caixa": valuation_fluxo_caixa,
            }
        )
        return response_invoke
