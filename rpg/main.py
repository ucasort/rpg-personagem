from __future__ import annotations
from typing import Dict, Type
from rpg.atributos import Atributos, EstiloDistribuicao
from rpg.racas import Humano, Anao, Elfo, Raca
from rpg.classes import Guerreiro, Mago, Ladino, Classe
from rpg.personagem import Personagem

def escolher(opcoes: Dict[int, str]) -> int:
    while True:
        try:
            valor = int(input("> "))
            if valor in opcoes:
                return valor
        except ValueError:
            pass
        print("Opção inválida. Tente novamente.")

def menu():
    print("=== CRIAÇÃO DE PERSONAGEM ===")

    # 1) estilo de atributos
    estilos = {
        1: ("Clássico (3d6 por atributo)", EstiloDistribuicao.CLASSICO),
        2: ("Heróico (4d6 descartando o menor)", EstiloDistribuicao.HEROICO),
        3: ("Aventureiro (array 15,14,13,12,10,8)", EstiloDistribuicao.AVENTUREIRO),
    }
    print("\nEscolha o estilo de distribuição de atributos:")
    for k, (desc, _) in estilos.items():
        print(f"{k}) {desc}")
    idx = escolher({k: v[0] for k, v in estilos.items()})
    estilo = estilos[idx][1]

    atributos = Atributos.distribuir(estilo)
    print(f"\nAtributos gerados: {atributos}\n")

    # 2) raça
    racas_map: Dict[int, Raca] = {
        1: Humano(),
        2: Anao(),
        3: Elfo(),
    }
    print("Escolha a raça:")
    for k, r in racas_map.items():
        print(f"{k}) {r.nome}")
    idx_r = escolher({k: r.nome for k, r in racas_map.items()})
    raca = racas_map[idx_r]

    # 3) classe
    classes_map: Dict[int, Classe] = {
        1: Guerreiro(),
        2: Mago(),
        3: Ladino(),
    }
    print("\nEscolha a classe:")
    for k, c in classes_map.items():
        print(f"{k}) {c.nome}")
    idx_c = escolher({k: c.nome for k, c in classes_map.items()})
    classe = classes_map[idx_c]

    nome = input("\nDigite o nome do personagem: ").strip() or "Sem Nome"
    p = Personagem(nome=nome, raca=raca, classe=classe, atributos=atributos)
    print("\n" + p.ficha())

if __name__ == "__main__":
    menu()
