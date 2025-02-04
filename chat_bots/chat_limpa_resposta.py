from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from chat_bots import get_secret_key
from pydantic import SecretStr
from langchain_core.prompts import PromptTemplate

load_dotenv()

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc

load_dotenv()


def ChatLimpaResposta(
    query: str,
    ticke: str,
    api_secret: SecretStr | None = api_secret_groq,
    modelo_llm: str = "llama-3.2-11b-vision-preview",
) -> str:
    model = ChatGroq(
        api_key=api_secret,
        model=modelo_llm,
        temperature=0.5,
        stop_sequences=None,
    )

    prompt = PromptTemplate(
        input_variables=["dados", "tick"],
        template="""
                You will receive a Markdown document containing news articles about various companies. Your task is to extract and summarize only the relevant information related to {tick} while removing unnecessary elements such as formatting, links, images, or irrelevant content.
                Avoid any responses indicating the absence of data or requests for additional input.
                Please provide detailed information about {tick}, focusing on significant news and updates about the company,
                without including generic comments, absence of data, or irrelevant information
                Less than 6500 characters in length.
                Structured in Markdown format without unnecessary empty lines.
                
                Avoid informations how: 
                "Nenhuma informação encontrada" or 
                "Nenhuma informação encontrada." or
                "Não consegui encontrar informações suficientes sobre a empresa {tick} nos artigos fornecidos."
                
                If no information about the company is found in the articles, do not mention it or provide any response.
                Deliver a clean, well-structured Markdown output with concise and meaningful information.
                Provide only the information from the news articles.
                                                    
                                                                                                   
        REQUESTED ANALYSIS:
        Dados: {dados}
        Tick: {tick}
        
        If no information about the company is found in the articles, do not mention it or provide any response. 
        Present only the extracted information concisely and clearly
        Always response the questions in Portuguese.

      """,
    )

    llm_chain = prompt | model | StrOutputParser()

    resposta = llm_chain.invoke(input={"dados": query, "tick": ticke})

    return resposta
