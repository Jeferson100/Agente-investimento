from typing import Any, LiteralString, Generator, Union, List
import pandas as pd


def generator_to_string(
    generator: Generator[Any, Any, Any],
) -> tuple[LiteralString, list[Any]]:
    """Converte um generator para uma string, preservando os chunks individuais."""
    chunks = []
    for chunk in generator:
        # Adapte isso de acordo com o formato do seu chunk
        if hasattr(chunk, "content"):
            chunk_text = chunk.content
        elif hasattr(chunk, "text"):
            chunk_text = chunk.text
        else:
            chunk_text = str(chunk)

        chunks.append(chunk_text)

    # Une todos os chunks em uma única string
    return "".join(chunks), chunks


def string_to_generator(
    string_or_chunks: Union[str, list[Any]],
) -> Generator[str, Any, Any]:
    """Converte uma string ou lista de chunks de volta para um generator."""
    if isinstance(string_or_chunks, str):
        # Se for uma string única, retorna um generator que produz apenas essa string
        yield string_or_chunks
    else:
        # Se for uma lista de chunks, cria um generator que produz cada chunk
        for chunk in string_or_chunks:
            yield chunk


def configurar_mensagem(response: str) -> str:
    text = "".join(list(response))
    if "</think>" in text:
        parts = text.split("</think>")
        if len(parts) > 1:
            return parts[1]  # Retorna o que vem depois de "</think>"

    return text


def retransfromando_pandas(trat: List[Any]) -> pd.DataFrame:
    df = pd.DataFrame([doc.metadata for doc in trat])

    df["data"] = [doc.page_content for doc in trat]

    return df
