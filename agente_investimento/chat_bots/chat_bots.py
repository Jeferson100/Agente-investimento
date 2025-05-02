from typing import Any, Dict, Iterator, List

from langchain.chains import LLMChain  # pylint: disable=E0611
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from .chat_groq import get_llm
from pydantic import SecretStr


class ChatBot:
    def __init__(
        self,
        query: str,
        dados: List[str],
        prompt_template: PromptTemplate,
        api_secret: SecretStr | None,
        name_query: str = "query",
        name_dados: str = "dados",
        temperature: float = 0.5,
        modelo_llm: str = "llama-3.3-70b-versatile",
        
    ):
        self.query = query
        self.name_query = name_query
        self.dados = dados
        self.name_dados = name_dados
        self.api_secret = api_secret
        self.temperature = temperature
        self.modelo_llm = modelo_llm
        self.prompt_template = prompt_template

    def model_chat(self) -> ChatGroq:
        return get_llm(
            api_groq=self.api_secret,
            model=self.modelo_llm,
            temperature=self.temperature,
            stop_sequences=None,
        )

    def llm_chain(self) -> LLMChain:
        return LLMChain(
            prompt=self.prompt_template,
            llm=self.model_chat(),
            output_parser=StrOutputParser(),
        )

    def invoke(self) -> Dict[str, Any]:
        result: Dict[str, Any] = self.llm_chain().invoke(
            input={self.name_query: self.query, self.name_dados: self.dados}
        )
        return result

    def stream(self) -> Iterator[str]:
        response_stream: Iterator[str] = self.llm_chain().stream(
            input={self.name_query: self.query, self.name_dados: self.dados}
        )
        return response_stream
