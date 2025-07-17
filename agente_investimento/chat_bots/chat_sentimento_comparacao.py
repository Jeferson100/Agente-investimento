from typing import Iterator

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import SecretStr

from .chat_groq import get_llm



async def ChatSentimentoComparacao(
    query: str,
    noticia: str,
    api_secret: SecretStr | None,
    temperature: float = 0.5,
    modelo_llm: str = "deepseek-r1-distill-llama-70b",
    stream: bool = False,
) -> str | Iterator[str]:
    prompt = PromptTemplate(
        input_variables=["query", "noticias"],
        template="""
    You are an investment analyst specializing in Natural Language Processing (NLP). .
    Task:
        Analyze the provided technical data {noticia} and answer the user's question {query}.
        Keep your response under 1000 characters and focus on key comparative insights.
        
Available Input:
- Multiple sets of recent news articles (headlines, summaries, or full articles) about different companies.
- Put '#########Sentiment Analysis Comparison#####' at the beginning of the answer

REQUESTED ANALYSIS:
Question: {query}
Financial News Data: {noticia}

Format the response with clear sections for each company..

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
        response_stream = llm_chain.stream(input={"query": query, "noticia": noticia})
        return response_stream

    else:
        response_invoke = await llm_chain.ainvoke(
            input={"query": query, "noticia": noticia}
        )
        return response_invoke
