import random
from typing import List, Tuple

def rolar_xdY(qtd: int, faces: int) -> List[int]:
    """Rola 'qtd' dados de 'faces' lados e retorna a lista de rolagens."""
    return [random.randint(1, faces) for _ in range(qtd)]

def soma_maiores(valores: List[int], k: int) -> int:
    """Soma os k maiores valores de uma lista."""
    return sum(sorted(valores, reverse=True)[:k])

def rolagem_classica_3d6() -> Tuple[List[int], int]:
    """Retorna (lista_rolagens, total) para 3d6."""
    r = rolar_xdY(3, 6)
    return r, sum(r)

def rolagem_heroica_4d6_drop_low() -> Tuple[List[int], int]:
    """Retorna (lista_rolagens, total_top3) para 4d6 descartando a menor."""
    r = rolar_xdY(4, 6)
    return r, soma_maiores(r, 3)
