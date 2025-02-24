from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from chat_bots import get_secret_key
from pydantic import SecretStr
from typing import Iterator
from langchain_core.rate_limiters import InMemoryRateLimiter

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc


def ChatValuation(
    query: str,
    precos_atual_valuations: str,
    indicadores_valuation_fluxo: str,
    valuation_metodo_gordon: str,
    valuation_fluxo_caixa: str,
    api_secret: SecretStr | None = api_secret_groq,
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
        You are an agent specialized in company valuation, responsible for determining whether a company is undervalued or overvalued.

        To achieve this, you receive two valuation estimates:
        1️ Discounted Cash Flow (DCF) Valuation
        2️ Gordon Growth Model Valuation (Perpetual Growth)

        Additionally, you have access to the current stock price, allowing you to compare the estimates with the market value.

        Data Description
        1. Stock Values
        You receive the current stock price and the estimated values from both valuation methods.

        2. Gordon Growth Model Valuation

        Based on the sustainable growth of dividends over time.
        The data includes median dividend, risk-free rate, beta, CAPM, sustainable growth rate, and estimated stock valuation.
        
        3. Discounted Cash Flow (DCF) Valuation

        Based on the projection of future cash flows, discounted to present value.
        The data includes annual revenue, EBIT, tax, CAPEX, depreciation, cash flow, and present value of future cash flows.
        
        4. Inputs Used for DCF Calculation

        Indicators used in the projection, such as EBIT margin, last reported revenue, revenue variation, depreciation-to-CAPEX ratio, CAPEX-to-revenue ratio, WACC, number of shares, total debt, available cash, other assets, liabilities, and working capital requirements.
        Model Task
        
        1. Comparison Between Valuation Methods

        Is the valuation from the Gordon Growth Model close to the valuation from the Discounted Cash Flow method?
        If there is a significant difference, what factors might be influencing this discrepancy?
        
        2. Profitability and Financial Sustainability Analysis

        Does the company have a positive or negative cash flow over the projected years?
        Is CAPEX excessively high, potentially compromising future cash flow?
        Does the company’s value generation justify the calculated valuation?
        
        3. Risks and Inconsistencies

        Are revenue and EBIT growth rates sustainable, or do they suggest a possible overestimation?
        Is the level of debt concerning? Does the debt-to-cash ratio indicate financial risks?
        Is the WACC appropriate for discounting future cash flows?
        
        4. Conclusion and Recommendation

        Based on the calculations, is the company undervalued or overvalued?
        What would be a recommendation for investors based on the analyzed data?
        Expected Response Format
        The model must provide a structured and objective analysis, answering each question based on the given data.
        The response should include numerical comparisons, justifications for discrepancies between valuation methods, and considerations on financial risks.

        REQUESTED ANALYSIS:
        Question: {query}
        Precos dos valuations e atual: {precos_atual_valuations}
        Inputs passado para estimar fluxo de caixa: {indicadores_valuation_fluxo}
        Valuation Fluxo Caixa: {valuation_fluxo_caixa}
        Valuation Metodo Gordon: {valuation_metodo_gordon}    
        
        Always response the questions in Portuguese.

      """,
    )

    rate_limiter = InMemoryRateLimiter(
        requests_per_second=0.1,
        check_every_n_seconds=0.1,
        max_bucket_size=10,
    )

    model = ChatGroq(
        api_key=api_secret,
        model=modelo_llm,
        # model="llama-3.2-11b-vision-preview",
        temperature=temperature,
        stop_sequences=None,
        rate_limiter=rate_limiter,
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
