from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from chat_bots import ChatAnaliseTecnica
from tratando_dados import TratandoDadosIndicadores
from chat_bots import get_secret_key
from pydantic import SecretStr
from typing import Iterator, List, Any
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.channels import Topic
import warnings
warnings.filterwarnings('ignore')

load_dotenv()

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc

api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    api_key=api_key,
    model="qwen-2.5-coder-32b",
    temperature=0,
    stop_sequences=None,
)

memory = MemorySaver()

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    # RETIRE THE TICKER DO PROMPT INITIAL
    messages: Annotated[list, add_messages]
    ticker: str 
    method_analysis: str  
    
    
class ModeloAnaliseTecnica():
    def __init__(
        self,
        state: State,
        periodo: str = "18Y",
        intervalo: str = "1mo",
        modelo_llm: str = "deepseek-r1-distill-llama-70b",
        stream: bool = True,
        api_secret: SecretStr | None = api_secret_groq,
    ) -> None:
        messages = state.get('messages', [])
    
        # Verifica se há mensagens
        if not messages:
            raise ValueError("Nenhuma mensagem encontrada no estado")
        
        # Encontra a última mensagem do usuário
        user_messages = [msg for msg in messages if isinstance(msg, HumanMessage)]
        
        if not user_messages:
            raise ValueError("Nenhuma mensagem do usuário encontrada no estado")
        
        # Pega a última mensagem do usuário
        last_message = user_messages[-1]
        
        self.query = last_message.content
        
        self.ticker = state.get('ticker')
        self.periodo = periodo
        self.intervalo = intervalo
        self.modelo_llm = modelo_llm
        self.stream = stream
        self.api_secret = api_secret

    def dados_indicadores_tecnicas(self) -> List[Any]:
        ind = TratandoDadosIndicadores(
            ticker=self.ticker, periodo=self.periodo, intervalo=self.intervalo
        )
        return ind.indicadores_data_loader()

    def chat_analise_tecnica(self) -> str | Iterator[str]:
        dados_tecnicas = self.dados_indicadores_tecnicas()
        response = ChatAnaliseTecnica(
            query=self.query,
            dados=dados_tecnicas,
            api_secret=self.api_secret,
            modelo_llm=self.modelo_llm,
            stream=self.stream,
        )
        return response
    

def process_technical(state: State) -> State:
    try:
        modelo = ModeloAnaliseTecnica(state=state)
        response = modelo.chat_analise_tecnica()
        new_state = state.copy()
        new_state["messages"].append(AIMessage(content=response)) 
        return new_state
    except Exception as e:
        pass
    
def chat_input(state: State) -> State:
    # Template do prompt
    prompt = """
    Você é um assistente especializado em investimentos. Por favor, extraia as seguintes informações da mensagem do usuário:
    1. O ticker (código) da ação
    2. O método de análise desejado (fundamentals, valuation, sentimental, technical)
    3. Se não houver o método, retorne chatbot para continuar a conversa
    
    Responda apenas com o ticker e o método no formato:
    TICKER: <ticker>
    MÉTODO: <método>
    """
    
    # Pegar a última mensagem do usuário
    last_message = state["messages"][-1]
    
    
    # Fazer a chamada ao LLM
    response = llm.invoke([
        HumanMessage(content=prompt),
        HumanMessage(content=last_message.content)
    ])
    
    response_text = response.content
    
    for line in response_text.split('\n'):
        if line.startswith('TICKER:'):
            state['ticker'] = line.split(':')[1].strip()
        elif line.startswith('MÉTODO:'):
            state['method_analysis'] = line.split(':')[1].strip()   
    
    return state

def should_continue(state: State):
    if state["method_analysis"] == "technical":
        return 'technical'
    return "chatbot"

graph_builder = StateGraph(State)

def chatbot(state: State) -> dict:
    """
    Processa as mensagens do usuário e retorna uma resposta formatada.
    """
    try:
        # Criar o prompt do sistema
        system_message = SystemMessage(content="""
        Você é um assistente especializado em análise de investimentos.
        Ajude o usuário com análises e informações sobre investimentos.
        Se não for perguntado nada de investimentos, volte ao chatbot e converse normalmente.
        
        """)
        
        # Pegar a última mensagem do usuário
        last_message = state["messages"][-1]
        
        
        # Montar a lista de mensagens para o LLM
        messages = [
            system_message,
            HumanMessage(content=f"{last_message.content}")
        ]
        
        # Fazer a chamada ao LLM
        response = llm.invoke(messages)
        
        # Retornar o estado atualizado
        return {
            "messages": [AIMessage(content=response.content)],
            "ticker": state.get("ticker", ""),
            "method_analysis": state.get("method_analysis", ""),
        }
        
    except Exception as e:
        return {
            "messages": [AIMessage(content=f"Erro no processamento: {str(e)}")],
            "ticker": state.get("ticker", ""),
            "method_analysis": state.get("method_analysis", ""),
 
        }
        
memory = MemorySaver()

graph_builder.add_node("chat_input", chat_input)
graph_builder.add_node("technical", process_technical)
graph_builder.add_node("chatbot", chatbot)
graph_builder.set_entry_point("chat_input")
graph_builder.add_conditional_edges(
    "chat_input",
    should_continue,
    {
        "technical": "technical",
        "chatbot": "chatbot",        
    },
)

#graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chat_input", "technical") 
graph_builder.add_edge("technical", "chatbot")
graph_builder.add_edge("chat_input", 'chatbot')
graph_builder.add_edge("technical", END)
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile(checkpointer=memory)

if __name__ == "__main__":
    user_input = "Bom dia tudo bem"

    # Configuração inicial do estado
    initial_state = {
        "messages": [HumanMessage(content=user_input)],
        "ticker": "",  # Definindo o ticker explicitamente
        "method_analysis": "" , # Definindo o método de análise|
        "done": False 
        
    }

    # Configuração do stream
    config = {"configurable": {"thread_id": "1"}}

    # Executando o grafo
    events = graph.invoke(
        initial_state,
        config=config,
        stream_mode="values",
    )