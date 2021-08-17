# -*- coding: utf-8 -*-
import copy
import functools
import math
import time
import traceback

from typing import List

from Posicao import Posicao
from AEstrela import AEstrela
from QuebraCabeca import QuebraCabeca
from QuebraCabecaImp import QuebraCabecaImp


def distQuarteirao(a: tuple, b: tuple):
    return abs(a[0] - b[0]) + abs((a[1] - b[1]))


def printError(ex, near_dist, near_dist_score, qc):
    print(f"""\u001b[31m
╔═════════════════╗
║ Houve um Error: ║
╚═════════════════╝
{qc.toString()}
╔════════════════════════════
║Error: {ex}
║stack: {traceback.format_exc()}
║Nearst_dist: {near_dist}
║Nearst_dist_score: {near_dist_score}
╚════════════════════════════\u001b[0m
""")


def getInvCount(arr):
    inv_count = 0
    for i in range(0, 9):
        for j in range(i + 1, 9):

            if arr[j] != -1 and arr[i] != -1 and arr[i] > arr[j]:
                inv_count += 1
    return inv_count


def isSolvable(puzzle):
    inv_count = getInvCount([j for sub in puzzle for j in sub])

    return inv_count % 2 == 0


class Node:
    def __init__(self, f, number, actual_pos):
        self.is_exploring: bool = False
        self.was_explored: bool = False
        self.f_value = f
        self.number = number
        self.actual_pos = actual_pos

    def __str__(self):
        return f"({self.number}: {self.f_value})"


class InternalBranch:
    def __init__(self, father_index, tab_state):
        self.nodes: List[Node] = []
        self.exploring_number = -1
        self.father_index = father_index
        self.tab_state = tab_state

    def __str__(self):
        return str(', '.join(str(e) for e in self.nodes))


class PseudoTree:
    TRUNK: List[InternalBranch] = []
    RIGHT_POSITION = {
        1: (0, 0),
        2: (0, 1),
        3: (0, 2),
        4: (1, 0),
        5: (1, 2),
        6: (2, 0),
        7: (2, 1),
        8: (2, 2),
    }

    def searchLessEqualThanActual(self, new_f_value) -> (Node, InternalBranch):
        for i in reversed(self.TRUNK):
            for j in i.nodes:
                if not j.is_exploring and not j.was_explored and j.f_value <= new_f_value:
                    return j, i
        return None, None

    def backtrack(self, back_branch: InternalBranch, back_node: Node):
        self.TRUNK = self.TRUNK[:back_branch.father_index + 1]

        for i in self.TRUNK[back_branch.father_index].nodes:
            if i.is_exploring:
                i.is_exploring = False
                i.was_explored = True
            if i == back_node:
                self.TRUNK[back_branch.father_index].exploring_number = i.number
                i.is_exploring = True

    @staticmethod
    def calcHeuristica(tab: QuebraCabecaImp):
        result = 0
        for linha, i in enumerate(tab.getTab()):
            for coluna, j in enumerate(i):
                if j == -1:
                    continue
                result += distQuarteirao((linha, coluna), PseudoTree.RIGHT_POSITION[j])

        return result

    @staticmethod
    def calculatingFValue(pos_move: tuple, empty_loc: tuple, tab: QuebraCabecaImp):

        tab.move(empty_loc[0], empty_loc[1], pos_move[0], pos_move[1])

        return PseudoTree.calcHeuristica(tab)


def simulaGame(qc: QuebraCabecaImp, solution: List[Posicao]):
    count = 0
    while not qc.isOrdenado():
        print("\033[2J")
        print("\033[0;0f")
        empty_loc = qc.getPosVazio()
        pos = solution[count]
        count += 1
        qc.move(empty_loc.getLinha(), empty_loc.getColuna(), pos.getLinha(), pos.getColuna())
        print(qc.toString())
        time.sleep(0.4)


class AEstrelaImp(AEstrela):

    def getSolucao(self, qc: QuebraCabecaImp):

        if not isSolvable(qc.getTab()):
            print("\u001b[1m\u001b[31mNão é possível solucionar o problema (⌣́_⌣̀)\u001b[0m")
            return []

        tree = PseudoTree()
        while not qc.isOrdenado():
            # Inicio do ciclo
            tab = qc.getTab()
            empty_loc = qc.getPosVazio().toTuple()
            best_node = None
            best_score = 100
            new_branch = InternalBranch(father_index=len(tree.TRUNK), tab_state=tab)

            for i in qc.getMovePossiveis():
                loc = i.toTuple()
                number = tab[loc[0]][loc[1]]

                if len(tree.TRUNK) > 0 and tree.TRUNK[-1].exploring_number == number:
                    continue

                node = Node(
                    f=tree.calculatingFValue(loc, empty_loc, qc),
                    number=number,
                    actual_pos=loc
                )

                qc.setTab(tab)  # Retornando tabuleiro ao estado inicial do ciclo

                new_branch.nodes.append(node)

                if node.f_value < best_score:
                    best_node = node
                    best_score = node.f_value

            back_node, back_branch = tree.searchLessEqualThanActual(best_score)

            if back_node is None:
                best_node.is_exploring = True
                new_branch.exploring_number = best_node.number
                tree.TRUNK.append(new_branch)
            else:
                tree.backtrack(back_branch, back_node)
                best_node = back_node
                qc.setTab(back_branch.tab_state)
                empty_loc = qc.getPosVazio().toTuple()

            try:
                qc.move(empty_loc[0], empty_loc[1], best_node.actual_pos[0], best_node.actual_pos[1])
            except Exception as ex:
                printError(ex, best_node, best_score, qc)
                break

        print("\u001b[1m\u001b[32mO PROBLEMA FOI SOLUCIONADO!!!＼(＾O＾)／\u001b[0m")
        arr = []
        append = arr.append
        for i in tree.TRUNK:
            for j in i.nodes:
                if j.is_exploring:
                    append(Posicao(j.actual_pos[0], j.actual_pos[1]))
        return arr
