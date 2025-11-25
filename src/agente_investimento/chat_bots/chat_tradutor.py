from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import SecretStr

from .chat_groq import get_llm


def ChatTradutor(
    query: str,
    api_secret: SecretStr | None,
    modelo_llm: str = "llama-3.2-11b-vision-preview",
) -> str:
    model = get_llm(
        api_groq=api_secret,
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
