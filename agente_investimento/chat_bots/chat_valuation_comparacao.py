from typing import Dict, Iterator

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import SecretStr

from .chat_groq import get_llm


async def ChatValuationComparacao(
    query: str,
    valuation_metodo_gordon: Dict[str, str],
    valuation_fluxo_caixa: Dict[str, str],
    api_secret: SecretStr | None,
    temperature: float = 0.5,
    modelo_llm: str = "deepseek-r1-distill-llama-70b",
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
    You are a specialized valuation agent responsible for comparing and analyzing multiple stocks to determine their relative value and investment potential. You receive valuation estimates and current stock prices for multiple companies:

    1. Gordon Growth Model Data (for each company):
    - Median dividend, risk-free rate, beta, CAPM, sustainable growth
    - Estimated stock price based on dividend growth

    2. Discounted Cash Flow (DCF) Model Data (for each company):
    - Annual revenue, EBIT, tax, CAPEX, depreciation
    - Cash flow projections and present values
    - Key inputs: EBIT margin, revenue variation, depreciation-to-CAPEX ratio
    - Financial metrics: WACC, shares outstanding, debt levels, cash position

    Your Comparative Analysis Tasks:

    1. Valuation Methods Comparison:
    - Compare Gordon Growth and DCF valuations for each stock
    - Identify which stocks show the largest discrepancies between methods
    - Analyze why certain stocks might have more reliable valuations

    2. Cross-Company Analysis:
    - Rank companies by their valuation metrics
    - Compare current market prices to estimated fair values
    - Identify which stocks appear most under/overvalued

    3. Financial Health Comparison:
    - Compare cash flow generation capabilities
    - Analyze relative CAPEX requirements and efficiency
    - Compare debt levels and financial strength

    4. Risk Assessment:
    - Compare growth sustainability across companies
    - Analyze relative debt-to-cash positions
    - Evaluate WACC appropriateness for each company

    5. Investment Recommendations:
    - Rank stocks by investment attractiveness
    - Provide relative value comparison
    - Identify best opportunities in the group

    REQUESTED ANALYSIS:
    Question: {query}
    DCF Valuation: {valuation_fluxo_caixa}
    Gordon Growth Valuation: {valuation_metodo_gordon}

    Format your response:
    1. Begin with '############Valuation Analysis############'
    2. Provide comparative tables where appropriate
    3. Include confidence level for each company analysis
    4. Keep total response within 1000 characters
    5. Present a clear ranking of investment opportunities

    The analysis should focus on relative value and comparative advantages/disadvantages between the stocks.
            """,
    )

    model = get_llm(
        api_groq=api_secret,
        model=modelo_llm,
        temperature=temperature,
        stop_sequences=None,
    )

    llm_chain = prompt | model | StrOutputParser()

    if stream:
        response_stream = llm_chain.stream(
            input={
                "query": query,
                "valuation_metodo_gordon": valuation_metodo_gordon,
                "valuation_fluxo_caixa": valuation_fluxo_caixa,
            },
        )
        return response_stream

    else:
        response_invoke = await llm_chain.ainvoke(
            input={
                "query": query,
                "valuation_metodo_gordon": valuation_metodo_gordon,
                "valuation_fluxo_caixa": valuation_fluxo_caixa,
            }
        )
        return response_invoke
