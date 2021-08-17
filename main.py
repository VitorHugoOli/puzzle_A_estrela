# -*- coding: utf-8 -*-

import datetime
from Posicao import Posicao
from AEstrelaImp import AEstrelaImp, simulaGame
from QuebraCabecaImp import QuebraCabecaImp

INIT_TAB = [
    [[7, 2, 1], [3, 4, 8], [6, QuebraCabecaImp.VAZIO, 5]],
    [[7, 2, 4], [8, 3, 1], [5, QuebraCabecaImp.VAZIO, 6]],
    [[7, 2, 4], [5, QuebraCabecaImp.VAZIO, 6], [8, 3, 1]],
    [[7, 2, 4], [1, QuebraCabecaImp.VAZIO, 5], [8, 3, 6]],
    [[1, 2, 3], [4, QuebraCabecaImp.VAZIO, 5], [6, 7, 8]],
    [[5, 6, 7], [4, QuebraCabecaImp.VAZIO, 8], [3, 2, 1]],  # Worst Case
    [[2, 8, 1], [4, 6, 3], [QuebraCabecaImp.VAZIO, 7, 5]],  # Hard Case
    [[2, 8, 1], [QuebraCabecaImp.VAZIO, 4, 3], [7, 6, 5]],  # Medium Case
    [[8, 1, 2], [QuebraCabecaImp.VAZIO, 4, 3], [7, 6, 5]],  # Exemplo sem solução (Not Solvable). Ref: https://www.geeksforgeeks.org/check-instance-8-puzzle-solvable/
]


# Realiza vários teste em sequência
def buck_tests():
    qc = QuebraCabecaImp()
    instance = AEstrelaImp()
    for index, i in enumerate(INIT_TAB):
        print(f"\u001b[1mCase {index}:\u001b[0m")
        tempo = datetime.datetime.now()
        qc.setTab(i)
        instance.getSolucao(qc)
        print("\u001b[1mTempo decorrido:\u001b[0m " + str(int((datetime.datetime.now() - tempo).total_seconds() * 100)) + " centesimos de segundos\n")


def main():
    print("Por favor, leia o readme antes de analisar o codigo ;)")
    qc = QuebraCabecaImp()
    instance = AEstrelaImp()

    tab = INIT_TAB[0]
    qc.setTab(tab)

    print("\u001b[1mTabuleiro inicial:\u001b[0m")
    print(qc.toString())

    tempo = datetime.datetime.now()
    result = instance.getSolucao(qc)
    print("\u001b[1mTempo decorrido:\u001b[0m " + str(int((datetime.datetime.now() - tempo).total_seconds() * 100)) + " centesimos de segundos")

    print("Movimentos")
    for pos in result:
        print("Linha: " + str(pos.getLinha()) + " - Coluna: " + str(pos.getColuna()))

    print("\u001b[1mTabuleiro final:\u001b[0m")
    print(qc.toString())

    is_simulate = input("Deseja simular o jogo ?\n1-Sim\n2-Não\n")
    if is_simulate == 1:
        qc.setTab(tab)
        simulaGame(qc, result)


main()
# buck_tests()
