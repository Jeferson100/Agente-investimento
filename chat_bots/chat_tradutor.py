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


def ChatTradutor(
    query: str,
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
        input_variables=["dados"],
        template="""
                
                Resuma o seguinte texto em inglês em até 1000 caracteres, mantendo as informações essenciais. 
                Em seguida, traduza apenas o resumo para o português. O resultado final deve conter somente o texto 
                resumido e traduzido, sem incluir o texto original ou qualquer outra informação adicional.                                     
                                                                                                   
        REQUESTED ANALYSIS:
        Dados: {dados}

      """,
    )

    llm_chain = prompt | model | StrOutputParser()

    resposta = llm_chain.invoke(input={"dados": query})

    return resposta
