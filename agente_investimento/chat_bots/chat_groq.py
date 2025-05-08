from langchain_groq import ChatGroq
from pydantic import SecretStr

from .verificacao_key import get_secret_key

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc


def get_llm(
    model: str = "meta-llama/llama-4-scout-17b-16e-instruct",
    api_groq: SecretStr | None = api_secret_groq,
    temperature: float = 0,
    stop_sequences: str | None = None,
) -> ChatGroq:
    """
    Returns a ChatGroq instance.
    """
    llm = ChatGroq(
        api_key=api_groq,
        model=model,
        temperature=temperature,
        stop_sequences=stop_sequences,
    )
    return llm
