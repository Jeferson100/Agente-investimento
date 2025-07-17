from typing import Iterator, List

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import SecretStr

from .chat_groq import get_llm

import os


async def ChatAnaliseTecnicaComparacao(
    query: str,
    dados: List[str],
    api_secret: SecretStr | None,
    temperature: float = 0.5,
    #modelo_llm: str = "llama-3.3-70b-versatile",
    modelo_llm: str = "meta-llama/llama-4-scout-17b-16e-instruct",                                                  
    stream: bool = False,
) -> str | Iterator[str]:
    prompt = PromptTemplate(
        input_variables=["query", "dados"],
        template="""
            
        You are an expert technical analyst with over 15 years of experience in comparative stock analysis. 

        Task:
        Analyze the provided technical data {dados} and answer the user's question {query}.
        Keep your response under 1000 characters and focus on key comparative insights.
    

        REQUESTED ANALYSIS:
        Question: {query}
        Technical Data: {dados}

        Response Format:
        1. Start with '#########Technical Analysis#######'

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
        response_stream = llm_chain.stream(input={"query": query, "dados": dados})
        return response_stream

    else:
        response_invoke = await llm_chain.ainvoke(
            input={"query": query, "dados": dados}
        )
        return response_invoke