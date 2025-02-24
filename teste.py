from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from chat_bots import get_secret_key
from pydantic import SecretStr
from langchain_core.prompts import PromptTemplate
from typing import Dict

load_dotenv()

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc

load_dotenv()


def ChatPegaTicker(
    query: str,
    dados_empresas:Dict[str,str],
    api_secret: SecretStr | None = api_secret_groq,
    modelo_llm: str = "llama3-8b-8192",
) -> str:
    model = ChatGroq(
        api_key=api_secret,
        model=modelo_llm,
        temperature=0.5,
        stop_sequences=None,
    )

    prompt = PromptTemplate(
        input_variables=["query", "dados_empresas"],
        template="""
        
                Você recebe a seguinte consulta: "{query}"
                
                Sua única missão é identificar o ticker da empresa mencionada, caso exista.

                Extraia o nome da empresa na consulta.
                Encontre seu código de negociação na bolsa de valores.
                Responda apenas com o ticker, sem qualquer outra informação adicional.
                Exemplo:
                Entrada: "O que você pode me dizer sobre o banco Bradesco?"
                Saída: BBDC4
                
                Voce recebe os nomes e o codigo na empresa no arquivo {dados_empresas}
                
                Utlize esse arquivo para identificar qual e o codigo da acao

            Se não encontrar um ticker válido, responda que nao encontrou.

      """,
    )

    llm_chain = prompt | model | StrOutputParser()

    resposta = llm_chain.invoke({'query':query, 'dados_empresas':dados_empresas})

    return resposta


if __name__ == "__main__":
    import json
    import time
    start = time.time()
    query = "O que você pode me dizer sobre o banco Petrobras?"
    with open('dados/empresas.json', 'r') as f:
        dados_empresas = json.load(f)
    print(ChatPegaTicker(query, dados_empresas))
    end = time.time()
    print(end - start)
    
