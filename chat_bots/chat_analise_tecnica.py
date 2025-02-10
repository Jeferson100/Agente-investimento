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


def ChatAnaliseTecnica(
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
            
            You are a technical analyst specialized in interpreting financial indicators to identify market trends, entry, and exit points. Use the following technical data to provide a detailed analysis of the current asset situation and a possible trading strategy:

            Available Indicators:
            Moving Averages
            20 periods:
            100 periods:
            200 periods:
            Relative Strength Index (RSI - 14 periods)
            MACD and Signal Line:
            MACD:
            Signal:
            Bollinger Bands:
            Upper:
            Middle:
            Lower:
            Support and Resistance Levels (Pivot Points):
            Pivot Point:
            Supports:
            Resistances:
            VWAP (Volume Weighted Average Price)
            ADX (Average Directional Index - 14 periods)
            Analysis Objectives:
            Trend Identification:
            Is the price above or below the moving averages?
            Do the moving averages indicate an uptrend or downtrend?
            Does the ADX indicate a strong trend (>25) or a weak trend (<25)?
            Market Strength:
            Does the RSI suggest overbought conditions (>70) or oversold conditions (<30)?
            Is the MACD crossing the signal line, suggesting a potential entry/exit point?
            Support and Resistance:
            Is the current price near a significant support or resistance level?
            Do the Bollinger Bands indicate high volatility (expansion) or low volatility (contraction)?
            Possible Strategy:
            If in an uptrend: Identify buying points and profit targets.
            If in a downtrend: Identify selling points and downside targets.
            If in a ranging market: Suggest reversal or breakout strategies.
            Based on these factors, provide a detailed analysis of the current asset situation and a recommended course of action (buy, sell, or wait).  

                                                                                                            
            REQUESTED ANALYSIS:
            Question: {query}
            Financial Data: {dados}
            
            
            Always response the questions in Portuguese.

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
        response_invoke = llm_chain.invoke(input={"query": query, "dados": dados})
        return response_invoke
