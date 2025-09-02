from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List
from .dados import rolar, rolar_4d6_descarta_menor

# Chaves padronizadas dos atributos (português abreviado)
CHAVES = ["FOR", "DES", "CON", "INT", "SAB", "CAR"]

class EstiloDistribuicao(Enum):
    CLASSICO = auto()      # 3d6 por atributo (3–18)
    HEROICO = auto()       # 4d6, descarta menor (6–18) – mais forte
    AVENTUREIRO = auto()   # Array heróico fixo (15,14,13,12,10,8) – escolha

def _array_heroico() -> List[int]:
    return [15, 14, 13, 12, 10, 8]

@dataclass
class Atributos:
    valores: Dict[str, int] = field(default_factory=lambda: {k: 10 for k in CHAVES})

    @staticmethod
    def distribuir(estilo: EstiloDistribuicao) -> "Atributos":
        v: Dict[str, int] = {}
        if estilo == EstiloDistribuicao.CLASSICO:
            # 3d6 para cada atributo
            for k in CHAVES:
                v[k] = rolar("3d6")
        elif estilo == EstiloDistribuicao.HEROICO:
            # 4d6 descartando menor
            for k in CHAVES:
                v[k] = rolar_4d6_descarta_menor()
        else:
            # AVENTUREIRO: array fixo distribuído automaticamente nas chaves
            array = _array_heroico()
            # estratégia simples: prioriza Físicos primeiro (FOR, DES, CON)
            ordem = ["FOR", "DES", "CON", "INT", "SAB", "CAR"]
            array.sort(reverse=True)
            v = {k: array[i] for i, k in enumerate(ordem)}
        return Atributos(v)

    def modificador(self, chave: str) -> int:
        return (self.valores[chave] - 10) // 2

    def aplicar_bonus(self, bonus: Dict[str, int]) -> None:
        for k, inc in bonus.items():
            if k in self.valores:
                self.valores[k] += inc

    def __str__(self) -> str:
        partes = []
        for k in CHAVES:
            mod = self.modificador(k)
            partes.append(f"{k}: {self.valores[k]} ({mod:+d})")
        return " | ".join(partes)
