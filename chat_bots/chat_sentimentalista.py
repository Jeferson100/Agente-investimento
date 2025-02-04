from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from chat_bots import get_secret_key
from pydantic import SecretStr

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc


def ChatSentimento(
    query: str,
    noticia: str,
    api_secret: SecretStr | None = api_secret_groq,
    temperature: float = 0.5,
    modelo_llm: str = "llama-3.2-11b-vision-preview",
) -> str:
    prompt = PromptTemplate(
        input_variables=["query", "noticias"],
        template="""
          You are an investment analyst specializing in Natural Language Processing (NLP). Your task is to evaluate the overall sentiment of recent news about a specific company and determine whether the current outlook is positive or negative for investment."

        📌 Model Input:
        A set of recent news articles about the company [COMPANY_NAME] collected from the internet.
        The news may include headlines, summaries, or full articles.
        
        Expected Output:
        1Sentiment Analysis
        For each news article, determine the predominant sentiment:
        Positive → Growth indicators, strong financial results, innovations, strategic acquisitions.
        Neutral → News with no direct impact or mixed information.
        Negative → Scandals, market declines, financial issues, internal crises.
        
        Assign a sentiment score (e.g., from -1 to +1).
        
        Overall Sentiment Score Calculation
        Based on the analyzed news, calculate an average sentiment index:
        Index ≥ +0.3 → Positive investment outlook.
        Index between -0.3 and +0.3 → Neutral outlook, caution advised.
        Index ≤ -0.3 → Negative outlook, not a good time to invest.
        
        Conclusion & Recommendation
        Is it a good time to invest?
        YES, positive outlook: Overall sentiment is favorable, and the company has good prospects.
        CAUTION, mixed outlook: There are uncertainties or market volatility.
        NO, negative outlook: Many negative news stories indicate high risk.     
                                                    
                                                                                                   
        REQUESTED ANALYSIS:
        Question: {query}
        Financial New Data: {noticia}
        
        Always response the questions in Portuguese.

      """,
    )

    model = ChatGroq(
        api_key=api_secret,
        # model="llama-3.3-70b-versatile",
        model=modelo_llm,
        temperature=temperature,
        stop_sequences=None,
    )

    llm_chain = prompt | model | StrOutputParser()

    response = llm_chain.invoke(input={"query": query, "noticia": noticia})

    return response
