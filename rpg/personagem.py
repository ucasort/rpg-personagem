from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
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
        # Aplica bônus raciais aos atributos
        self.atributos.aplicar_bonus(self.raca.bonus_atributos)

    @property
    def pv(self) -> int:
        # Para simplificar, consideramos apenas PV do 1º nível
        return max(1, self.classe.pv_nivel1(self.atributos))

    def ficha(self) -> str:
        atr = self.atributos
        linhas = [
            f"=== FICHA DE PERSONAGEM ===",
            f"Nome: {self.nome}",
            f"Raça: {self.raca.nome} | Movimento: {self.raca.movimento_m} m | "
            f"Infravisão: {self.raca.infravisao_m if self.raca.infravisao_m else '—'} m | "
            f"Alinhamento: {self.raca.alinhamento}",
            f"Classe: {self.classe.nome} (Dado de Vida d{self.classe.dado_vida})",
            f"Nível: {self.nivel} | PV (1º nível): {self.pv}",
            f"Atributos: {atr}",
            f"Atributos-chave da classe: {', '.join(self.classe.atributos_chave)}",
            f"Profic. Armas: {', '.join(self.classe.prof_armas) if self.classe.prof_armas else '—'}",
            f"Profic. Armaduras: {', '.join(self.classe.prof_armaduras) if self.classe.prof_armaduras else '—'}",
            f"Habilidades de Raça: {', '.join(self.raca.habilidades) if self.raca.habilidades else '—'}",
            f"Características de Classe: {', '.join(self.classe.caracteristicas) if self.classe.caracteristicas else '—'}",
        ]
        return "\n".join(linhas)
