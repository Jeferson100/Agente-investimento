from typing import Iterator, List

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import SecretStr

from .chat_groq import get_llm

async def ChatFundamentalistasComparacaoAsync(
    query: str,
    dados: List[str],
    api_secret: SecretStr | None,
    temperature: float = 0.5,
    modelo_llm: str = "meta-llama/llama-4-maverick-17b-128e-instruct",
    stream: bool = False,
) -> str | Iterator[str]:
    prompt = PromptTemplate(
        input_variables=["query", "dados"],
        template="""
    You are a fundamental analyst responsible for evaluating the financial health, operational performance, and investment prospects of multiple companies using key financial indicators. You will compare the companies to highlight relative strengths and weaknesses, and identify the best investment opportunity among them.

    Indicators provided include:

    Financial Results: revenue, gross profit, EBIT, EBITDA, net income, earnings per share.

    Cash Flows: operating, investing, financing, free cash flow (last three months).

    Investments/Expenses: CAPEX (last three months).

    Valuation: P/E, P/S, P/FCF, P/EBIT, EV/EBIT, EV/EBITDA, enterprise value, market cap.

    Dividends: dividend yield.

    Balance Sheet: total assets, gross debt, net debt, shareholders' equity, book value per share.

    Profitability & Efficiency: return on tangible capital, return on invested capital, return on equity, gross margin, net margin, asset turnover, financial leverage.

    Risks & Leverage: debt-to-equity ratio.

    Your Task:

    Compare the financial indicators of the companies.

    Identify each company's relative strengths and weaknesses.

    Determine which company is the most attractive investment and justify your decision.

    Provide a recommendation (buy, hold, or sell) for each company, with a confidence level (0–100%).

    Summarize trends and implications briefly.

    Begin your answer with '##########Fundamental Analysis########'.

    Limit your response to 1000 characters.

    REQUESTED ANALYSIS:
    Question: {query}
    Financial Data: {dados}
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
        response_stream = llm_chain.stream(input={"query": query, "dados": dados})
        return response_stream

    else:
        response_invoke = await llm_chain.ainvoke(
            input={"query": query, "dados": dados}
        )
        return response_invoke