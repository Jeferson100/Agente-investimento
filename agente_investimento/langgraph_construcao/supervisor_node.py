from typing import Literal

from ..chat_bots import get_llm

from langgraph.types import Command
from typing_extensions import TypedDict


from .state import State

# Defina os métodos de análise disponíveis
members = [
    "fundamentals",
    "technical",
    "sentimental",
    "valuation",
    "analise_investimento",
]
options = members + ["FINISH"]

system_prompt = (
    "Você é um supervisor de análise de investimentos. Sua tarefa é gerenciar "
    f"os seguintes métodos de análise: {members}. Dada a solicitação do usuário, "
    "decida qual próximo método de análise deve ser executado. Cada método "
    "realizará sua análise específica e reportará resultados. Quando todas "
    "as análises necessárias estiverem concluídas, responda com FINISH."
)


class Router(TypedDict):
    """Determina o próximo método de análise. Se nenhum método for necessário, encerra."""

    next: Literal[
        "fundamentals",
        "technical",
        "sentimental",
        "valuation",
        "analise_investimento",
        "FINISH",
    ]


def supervisor_node(
    state: State,
) -> Command[
    Literal[
        "fundamentals",
        "technical",
        "sentimental",
        "valuation",
        "analise_investimento",
        "chatbot",
    ]
]:
    """
    Executes the supervisor node, which decides which analysis method should be executed next.
    The supervisor node checks if there are still analysis methods available and, if so,
    uses a language model to determine which method should be executed next.
    If no analysis methods remain, the workflow is redirected to the chatbot node.

    Args:
        state (State): The current state dictionary, which must contain:
                       'method_analysis': A list of available analysis methods.

    Returns:
        Command: A command indicating the next node to be executed and updating the state.
                 If all analysis methods have been completed, it redirects to the chatbot node.
    """
    metodo_analise = state["method_analysis"]

    if not metodo_analise:
        print("Todos os métodos de análise concluídos")
        return Command(goto="chatbot")

    messages = [
        {"role": "system", "content": system_prompt},
    ] + metodo_analise

    context_message = (
        f"Métodos de análise disponíveis: {', '.join(state['method_analysis'])}. "
        "Escolha o próximo método a ser executado."
    )
    messages.append({"role": "system", "content": context_message})

    llm = get_llm(
        model="qwen-qwq-32b",
        temperature=0,
        stop_sequences=None,
    )

    try:
        response = llm.with_structured_output(Router).invoke(messages)  # type: ignore
        goto = response["next"]  # type: ignore
    except Exception as e:  # pylint: disable=W0718
        print(f"Erro na seleção do método: {e}")
        # Caso de erro, use o primeiro método disponível
        goto = state["method_analysis"][0]

    if goto not in state["method_analysis"]:
        goto = state["method_analysis"][0]

    remaining_methods = [m for m in state["method_analysis"] if m != goto]

    return Command(
        goto=goto, update={"method_analysis": remaining_methods, "next": goto}
    )
