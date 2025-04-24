from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from chat_bots import get_secret_key
from pydantic import SecretStr
from typing import List, Iterator

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc


async def ChatFundamentalistasAsync(
    query: str,
    dados: List[str],
    api_secret: SecretStr | None = api_secret_groq,
    temperature: float = 0.5,
    modelo_llm: str = "llama-3.3-70b-versatile",
    stream: bool = False,
) -> str | Iterator[str]:
    prompt = PromptTemplate(
        input_variables=["query", "dados"],
        template="""
                You are a fundamental analyst responsible for evaluating a company's financial health, operational performance, and investment prospects using key financial indicators. Your goal is to provide a concise analysis with actionable recommendations (buy, hold, or sell) along with a confidence level (0-100%).

    Indicators provided include:
    - Financial Results: revenue, gross profit, EBIT, EBITDA, net income, earnings per share.
    - Cash Flows: operating, investing, financing, free cash flow (last three months).
    - Investments/Expenses: CAPEX (last three months).
    - Valuation: P/E, P/S, P/FCF, P/EBIT, EV/EBIT, EV/EBITDA, enterprise value, market cap.
    - Dividends: dividend yield.
    - Balance Sheet: total assets, gross debt, net debt, shareholders' equity, book value per share.
    - Profitability & Efficiency: return on tangible capital, return on invested capital, return on equity, gross margin, net margin, asset turnover, financial leverage.
    - Risks & Leverage: debt-to-equity ratio.

    Your Task:
    - Analyze these indicators to identify the company’s strengths and weaknesses.
    - Generate actionable insights with a clear recommendation (buy, hold, or sell) and justify your decision.
    - Summarize trends and potential future implications.
    - Provide your answer concisely and include your confidence level.
    - Put '##########Fundamental Analysis########' at the beginning of the answer

    REQUESTED ANALYSIS:
    Question: {query}
    Financial Data: {dados}
    
    The response should be with the length of 1000 characters.
      """,
    )

    model = ChatGroq(
        api_key=api_secret,
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
        response_invoke = await llm_chain.ainvoke(input={"query": query, "dados": dados})
        return response_invoke