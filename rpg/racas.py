from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class Raca:
    nome: str
    movimento_m: float                # metros por turno
    infravisao_m: Optional[float]     # None se não possuir
    alinhamento: str
    habilidades: List[str] = field(default_factory=list)
    bonus_atributos: Dict[str, int] = field(default_factory=dict)

class Humano(Raca):
    def __init__(self):
        super().__init__(
            nome="Humano",
            movimento_m=9.0,
            infravisao_m=None,
            alinhamento="Qualquer",
            habilidades=["Versatilidade (+1 em todos os atributos)"],
            bonus_atributos={"FOR":1, "DES":1, "CON":1, "INT":1, "SAB":1, "CAR":1},
        )

class Anao(Raca):
    def __init__(self):
        super().__init__(
            nome="Anão",
            movimento_m=7.5,
            infravisao_m=18.0,
            alinhamento="Geralmente Leal",
            habilidades=[
                "Resiliência (vantagem contra veneno)",
                "Conhecimento de Minas e Metal"
            ],
            bonus_atributos={"CON":2},
        )

class Elfo(Raca):
    def __init__(self):
        super().__init__(
            nome="Elfo",
            movimento_m=9.0,
            infravisao_m=18.0,
            alinhamento="Geralmente Caótico Bom",
            habilidades=[
                "Sentidos Aguçados",
                "Transe (descanso reduzido)"
            ],
            bonus_atributos={"DES":2},
        )
