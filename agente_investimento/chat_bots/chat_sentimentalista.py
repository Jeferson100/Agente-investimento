from typing import Iterator

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from .chat_groq import get_llm
from pydantic import SecretStr



def ChatSentimento(
    query: str,
    noticia: str,
    api_secret: SecretStr | None,
    temperature: float = 0.5,
    modelo_llm: str = "llama-3.2-11b-vision-preview",
    stream: bool = False,
) -> str | Iterator[str]:
    prompt = PromptTemplate(
        input_variables=["query", "noticias"],
        template="""
         You are an investment analyst specializing in Natural Language Processing (NLP). Your task is to evaluate the overall sentiment of recent news about a specific company and determine whether the current investment outlook is positive or negative. Provide a concise answer in Portuguese including a recommendation and a confidence level (0-100%).

    Available Input:
    - A set of recent news articles (headlines, summaries, or full articles) about the company [COMPANY_NAME].
    - Put 'Sentiment Analysis' at the beginning of the answer

    Expected Output:
    1. For each article, determine the predominant sentiment:
    - Positive: growth indicators, strong financials, innovations, strategic acquisitions.
    - Neutral: mixed or no significant impact.
    - Negative: scandals, market declines, financial problems, internal crises.
    2. Assign a sentiment score to each article (range: -1 to +1).
    3. Calculate an overall average sentiment index:
    - Index ≥ +0.3 → Positive outlook.
    - Index between -0.3 and +0.3 → Neutral outlook, caution advised.
    - Index ≤ -0.3 → Negative outlook.
    4. Conclude with a clear recommendation (YES for positive, CAUTION for mixed, NO for negative).

    REQUESTED ANALYSIS:
    Question: {query}
    Financial News Data: {noticia}

    Always respond in Portuguese. Keep your answer concise and include your confidence level.

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
        response_invoke = llm_chain.invoke(input={"query": query, "noticia": noticia})
        return response_invoke
