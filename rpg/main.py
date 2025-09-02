from __future__ import annotations
from typing import Dict, List

# Imports robustos: funciona rodando como módulo OU como script direto
try:
    from .atributos import Atributos, EstiloDistribuicao, CHAVES
    from .racas import Humano, Anao, Elfo, Raca
    from .classes import Guerreiro, Mago, Ladino, Classe
    from .personagem import Personagem
except ImportError:
    from atributos import Atributos, EstiloDistribuicao, CHAVES
    from racas import Humano, Anao, Elfo, Raca
    from classes import Guerreiro, Mago, Ladino, Classe
    from personagem import Personagem

def escolher(opcoes: Dict[int, str]) -> int:
    while True:
        try:
            v = int(input("> "))
            if v in opcoes:
                return v
        except ValueError:
            pass
        print("Opção inválida. Tente novamente.")

def menu_aventureiro_ordem() -> List[str]:
    print("\nVocê quer escolher a ordem do array (15,14,13,12,10,8)?")
    print("1) Não, aplicar na ordem padrão: " + ", ".join(CHAVES))
    print("2) Sim, vou informar a ordem (ex: FOR DES CON INT SAB CAR)")
    op = escolher({1: "nao", 2: "sim"})
    if op == 1:
        return CHAVES[:]
    else:
        while True:
            texto = input("Digite a ordem separada por espaços: ").strip().upper()
            ordem = [t for t in texto.split() if t]
            if len(ordem) == len(CHAVES) and set(ordem) == set(CHAVES):
                return ordem
            print("Ordem inválida. Use as chaves: " + ", ".join(CHAVES))

def main():
    print("=== CRIAÇÃO DE PERSONAGEM ===")

    # 1) Estilo dos atributos
    print("\nEscolha o estilo de distribuição de atributos (pág. 14):")
    estilos = {
        1: "Clássico (3d6 por atributo)",
        2: "Aventureiro (array 15,14,13,12,10,8)",
        3: "Heróico (4d6 descartando a menor)"
    }
    for k, desc in estilos.items():
        print(f"{k}) {desc}")
    e = escolher(estilos)

    if e == 1:
        atributos = Atributos.distribuir(EstiloDistribuicao.CLASSICO)
    elif e == 2:
        ordem = menu_aventureiro_ordem()
        if ordem == CHAVES:
            atributos = Atributos.distribuir(EstiloDistribuicao.AVENTUREIRO)
        else:
            atributos = Atributos.distribuir_aventureiro_com_ordem(ordem)
    else:
        atributos = Atributos.distribuir(EstiloDistribuicao.HEROICO)

    print("\nAtributos gerados/alocados:")
    print(atributos.resumo())

    # 2) Raça
    racas_map: Dict[int, Raca] = {1: Humano(), 2: Anao(), 3: Elfo()}
    print("\nEscolha a raça:")
    for k, r in racas_map.items():
        print(f"{k}) {r.nome}")
    idx_r = escolher({k: r.nome for k, r in racas_map.items()})
    raca = racas_map[idx_r]

    # 3) Classe
    classes_map: Dict[int, Classe] = {1: Guerreiro(), 2: Mago(), 3: Ladino()}
    print("\nEscolha a classe:")
    for k, c in classes_map.items():
        print(f"{k}) {c.nome}")
    idx_c = escolher({k: c.nome for k, c in classes_map.items()})
    classe = classes_map[idx_c]

    nome = input("\nDigite o nome do personagem: ").strip() or "Sem Nome"

    p = Personagem(nome=nome, raca=raca, classe=classe, atributos=atributos)
    print("\n" + p.ficha())

if __name__ == "__main__":
    main()
