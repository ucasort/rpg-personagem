import random
from typing import List

def rolar(ndx: str) -> int:
    """Rola dados no formato 'XdY' (ex: '3d6')."""
    x, y = ndx.lower().split("d")
    return sum(random.randint(1, int(y)) for _ in range(int(x)))

def rolar_4d6_descarta_menor() -> int:
    rolagens: List[int] = [random.randint(1, 6) for _ in range(4)]
    rolagens.remove(min(rolagens))
    return sum(rolagens)
