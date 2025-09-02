from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List
from .dados import rolagem_classica_3d6, rolagem_heroica_4d6_drop_low

# Nomes/ordem dos atributos (ajuste se seu livro usar outra sigla)
CHAVES = ["FOR", "DES", "CON", "INT", "SAB", "CAR"]

class EstiloDistribuicao(Enum):
    CLASSICO = auto()       # 3d6 por atributo
    AVENTUREIRO = auto()    # array fixo (padrão abaixo), distribuído nas chaves
    HEROICO = auto()        # 4d6 descartando a menor

# Se o seu livro usar outro array, é só trocar aqui:
ARRAY_AVENTUREIRO_PADRAO = [15, 14, 13, 12, 10, 8]

@dataclass
class Atributos:
    valores: Dict[str, int] = field(default_factory=lambda: {k: 10 for k in CHAVES})
    origem: Dict[str, str]  = field(default_factory=dict)  # explica como saiu cada valor

    @staticmethod
    def distribuir(estilo: EstiloDistribuicao) -> "Atributos":
        valores: Dict[str, int] = {}
        origem: Dict[str, str]  = {}

        if estilo == EstiloDistribuicao.CLASSICO:
            # 3d6 por atributo
            for k in CHAVES:
                rolagens, total = rolagem_classica_3d6()
                valores[k] = total
                origem[k]  = f"3d6={rolagens}→{total}"

        elif estilo == EstiloDistribuicao.HEROICO:
            # 4d6 descartando a menor
            for k in CHAVES:
                rolagens, total = rolagem_heroica_4d6_drop_low()
                valores[k] = total
                origem[k]  = f"4d6{rolagens}→top3={total}"

        else:  # AVENTUREIRO
            arr = ARRAY_AVENTUREIRO_PADRAO[:]
            # estratégia simples: aplica na ordem CHAVES
            for k, v in zip(CHAVES, arr):
                valores[k] = v
                origem[k]  = f"array{ARRAY_AVENTUREIRO_PADRAO}"

        return Atributos(valores, origem)

    @staticmethod
    def distribuir_aventureiro_com_ordem(ordem_chaves: List[str]) -> "Atributos":
        """Permite o usuário escolher a ordem de alocação do array fixo."""
        if len(ordem_chaves) != len(CHAVES) or set(ordem_chaves) != set(CHAVES):
            raise ValueError("Ordem inválida das chaves de atributos.")
        valores: Dict[str, int] = {}
        origem: Dict[str, str]  = {}
        arr = ARRAY_AVENTUREIRO_PADRAO[:]
        for k, v in zip(ordem_chaves, arr):
            valores[k] = v
            origem[k]  = f"array{ARRAY_AVENTUREIRO_PADRAO}"
        return Atributos(valores, origem)

    def modificador(self, chave: str) -> int:
        return (self.valores[chave] - 10) // 2

    def __str.me__(self) -> str:  # só para evitar chamada acidental
        return self.resumo()

    def resumo(self) -> str:
        linhas = []
        for k in CHAVES:
            mod = self.modificador(k)
            linhas.append(f"{k}: {self.valores[k]} ({mod:+d})  [{self.origem.get(k, '')}]")
        return "\n".join(linhas)
