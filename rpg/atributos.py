from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple
from .dados import rolls, StdRandom

# Ordem canônica dos 6 atributos
ABILIDADES: Tuple[str, ...] = ("STR", "DEX", "CON", "INT", "WIS", "CHA")

def modificador(score: int) -> int:
    """Cálculo simples de modificador (compatível com tabelas comuns)."""
    return (score - 10) // 2

class MetodoDistribuicao(Enum):
    """
    Estilos de distribuição (página 14):
    - CLASSICO: 3d6 na ordem (sem redistribuir)
    - AVENTUREIRO: 3d6 x 6 e o jogador distribui como quiser
    - HEROICO: 4d6 descarta o menor, 6x, e distribui como quiser
    """
    CLASSICO = auto()
    AVENTUREIRO = auto()
    HEROICO = auto()

@dataclass(frozen=True)
class ConjuntoAtributos:
    STR: int
    DEX: int
    CON: int
    INT: int
    WIS: int
    CHA: int

    # ---------- utilidades ----------
    @classmethod
    def from_dict(cls, d: Dict[str,int]) -> "ConjuntoAtributos":
        return cls(*(d[a] for a in ABILIDADES))

    def as_dict(self) -> Dict[str,int]:
        return {k:getattr(self,k) for k in ABILIDADES}

    def mod(self, key: str) -> int:
        return modificador(getattr(self, key))

    # ---------- geradores conforme o livro ----------
    @staticmethod
    def _classico(rng: Optional[StdRandom] = None) -> "ConjuntoAtributos":
        """
        Estilo clássico: 3d6 para cada atributo, NA ORDEM (STR, DEX, CON, INT, WIS, CHA).
        """
        rng = rng or StdRandom()
        vals = [sum(rolls(6,3,rng)) for _ in ABILIDADES]
        return ConjuntoAtributos(*vals)

    @staticmethod
    def _aventureiro(rng: Optional[StdRandom] = None) -> List[int]:
        """
        Estilo aventureiro: rola 3d6 seis vezes e devolve a LISTA de 6 valores
        para o jogador distribuir livremente.
        (A distribuição efetiva é feita pelo método `reordenar` lá na main.)
        """
        rng = rng or StdRandom()
        return [sum(rolls(6,3,rng)) for _ in ABILIDADES]

    @staticmethod
    def _heroico(rng: Optional[StdRandom] = None) -> List[int]:
        """
        Estilo heróico: para cada valor, rola 4d6 e descarta o menor.
        Faz isso 6x e devolve a lista para distribuição.
        """
        rng = rng or StdRandom()
        resultados: List[int] = []
        for _ in ABILIDADES:
            r = rolls(6,4,rng)
            r.remove(min(r))
            resultados.append(sum(r))
        return resultados

    # ---------- API de alto nível ----------
    @classmethod
    def gerar(cls, metodo: MetodoDistribuicao, rng: Optional[StdRandom] = None,
              ordem: Optional[List[str]] = None) -> "ConjuntoAtributos":
        """
        - CLASSICO: ignora `ordem` e gera direto na sequência.
        - AVENTUREIRO / HEROICO: gera 6 valores e os distribui conforme `ordem` (se dada).
          Se `ordem` não for informada, mantém a ordem canônica (só para não travar).
        """
        if metodo == MetodoDistribuicao.CLASSICO:
            return cls._classico(rng)

        # A partir daqui, os dois estilos geram um pool de 6 valores
        pool = cls._aventureiro(rng) if metodo == MetodoDistribuicao.AVENTUREIRO else cls._heroico(rng)

        # Se o usuário passou uma ordem (ex.: ["STR","CON","DEX","INT","WIS","CHA"]),
        # vamos mapear os 6 valores do pool para essa ordem.
        # Convenção: o primeiro valor do pool vai para a primeira posição de `ordem`, etc.
        destino = ordem[:] if ordem else list(ABILIDADES)

        if len(destino) != 6 or any(a not in ABILIDADES for a in destino):
            raise ValueError("Ordem inválida: use exatamente os 6 nomes: STR DEX CON INT WIS CHA")

        # Monta um dict: atributo -> valor do pool correspondente
        atribuicoes = {destino[i]: pool[i] for i in range(6)}
        return ConjuntoAtributos.from_dict(atribuicoes)
