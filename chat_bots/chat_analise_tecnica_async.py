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


async def ChatAnaliseTecnicaAsync(
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
            
            You are a technical analyst specializing in interpreting financial indicators to identify market trends and determine entry/exit points. Based on the following technical data, provide a concise analysis of the current asset situation and recommend a trading strategy (buy, sell, or wait). In your response, please include a confidence level (0-100%) regarding your evaluation.

    Available Indicators:
    - Moving Averages (20, 100, 200 periods)
    - Relative Strength Index (RSI - 14 periods)
    - MACD and Signal Line
    - Bollinger Bands (Upper, Middle, Lower)
    - Support and Resistance Levels (Pivot Points)
    - VWAP (Volume Weighted Average Price)
    - ADX (14 periods)

    Analysis Objectives:
    - Trend Identification: Is the price above or below the moving averages? What trend (up, down, or sideways) is indicated?
    - Market Strength: Does the RSI suggest overbought (>70) or oversold (<30) conditions? Is the MACD crossing the signal line?
    - Volatility: Do the Bollinger Bands and ADX reflect high or low volatility?
    - Strategy: For trending markets, identify entry/exit points; for ranging markets, suggest reversal or breakout strategies.

    REQUESTED ANALYSIS:
    Question: {query}
    Financial Data: {dados}
    Put '#########Technical Analysis#######' at the beginning of the answer. keeping your answer concise and including your confidence level.
    The response should be with the length of 1000 characters.

        """,
    )

    model = ChatGroq(
        api_key=api_secret,
        model=modelo_llm,
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