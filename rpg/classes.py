from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from .atributos import Atributos

@dataclass
class Classe:
    nome: str
    dado_vida: int
    prof_armas: List[str]
    prof_armaduras: List[str]
    atributos_chave: List[str]
    caracteristicas: List[str] = field(default_factory=list)

    def pv_nivel1(self, atr: Atributos) -> int:
        """PV no 1º nível: dado de vida + mod CON."""
        return self.dado_vida + atr.modificador("CON")

class Guerreiro(Classe):
    def __init__(self):
        super().__init__(
            nome="Guerreiro",
            dado_vida=10,
            prof_armas=["Simples", "Marciais"],
            prof_armaduras=["Leve", "Média", "Pesada", "Escudos"],
            atributos_chave=["FOR", "CON"],
            caracteristicas=["Estilo de Luta", "Recuperar Fôlego"],
        )

class Mago(Classe):
    def __init__(self):
        super().__init__(
            nome="Mago",
            dado_vida=6,
            prof_armas=["Simples (bastão, adaga, etc.)"],
            prof_armaduras=[],
            atributos_chave=["INT"],
            caracteristicas=["Magia Arcana", "Truques"],
        )

class Ladino(Classe):
    def __init__(self):
        super().__init__(
            nome="Ladino",
            dado_vida=8,
            prof_armas=["Simples", "Leves de Finesse"],
            prof_armaduras=["Leve"],
            atributos_chave=["DES"],
            caracteristicas=["Ataque Furtivo", "Perícias", "Esquiva"],
        )
