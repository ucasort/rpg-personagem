from __future__ import annotations
from dataclasses import dataclass
from .atributos import Atributos
from .racas import Raca
from .classes import Classe

@dataclass
class Personagem:
    nome: str
    raca: Raca
    classe: Classe
    atributos: Atributos
    nivel: int = 1

    def __post_init__(self):
        # Aplica bônus raciais de atributo
        self.atributos.aplicar_bonus(self.raca.bonus_atributos)

    @property
    def pv(self) -> int:
        return self.classe.pv_nivel1(self.atributos)

    # Pequena utilidade para aplicar bônus (para não importar no professor)
    # Coloquei aqui para manter coeso com Personagem.
    def aplicar_bonus(self, bonus: dict) -> None:
        self.atributos.aplicar_bonus(bonus)

    def ficha(self) -> str:
        atr = self.atributos
        linhas = [
            "=== FICHA DE PERSONAGEM ===",
            f"Nome: {self.nome}",
            f"Raça: {self.raca.nome} | Movimento: {self.raca.movimento_m} m | "
            f"Infravisão: {self.raca.infravisao_m if self.raca.infravisao_m else '—'} m | "
            f"Alinhamento: {self.raca.alinhamento}",
            f"Classe: {self.classe.nome} (d{self.classe.dado_vida})",
            f"Nível: {self.nivel} | PV (1º nível): {self.pv}",
            f"Atributos:\n{atr.resumo()}",
            f"Atributos-chave da classe: {', '.join(self.classe.atributos_chave)}",
            f"Prof. Armas: {', '.join(self.classe.prof_armas) if self.classe.prof_armas else '—'}",
            f"Prof. Armaduras: {', '.join(self.classe.prof_armaduras) if self.classe.prof_armaduras else '—'}",
            f"Habilidades de Raça: {', '.join(self.raca.habilidades) if self.raca.habilidades else '—'}",
            f"Características de Classe: {', '.join(self.classe.caracteristicas) if self.classe.caracteristicas else '—'}",
        ]
        return "\n".join(linhas)
