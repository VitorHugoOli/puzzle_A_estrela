import math
import time
import traceback

from typing import List

from Posicao import Posicao
from AEstrela import AEstrela
from QuebraCabeca import QuebraCabeca
from QuebraCabecaImp import QuebraCabecaImp


def positionToTuple(pos: Posicao):
    return pos.getLinha(), pos.getColuna()


def dist2points(a: tuple, b: tuple):
    return math.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))


class Node:
    def __init__(self, f, number, actual_pos):
        self.select_to_gr: bool = False
        self.was_explored: bool = False
        self.f_value = f
        self.number = number
        self.actual_pos = actual_pos

    def __str__(self):
        return f"({self.number}: {self.f_value}),{self.select_to_gr},{self.was_explored}"


class InternalBranch:
    def __init__(self, father_index, tab_state):
        self.nodes: List[Node] = []
        self.exploring_number = -1
        self.father_index = father_index
        self.tab_state = tab_state

    def __str__(self):
        return str(', '.join(str(e) for e in self.nodes))


class AEstrelaImp(AEstrela):
    TREE: List[InternalBranch] = []

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

    # def searchLessThanActualDECRP(self, actual_node: Node, index):
    #     if index == -1:
    #         return None
    #
    #     for i in self.TREE[index]:
    #         if not i.select_to_gr and not i.was_explored and i.f_value < actual_node.f_value:
    #             return i
    #     return self.searchLessThanActual(actual_node, index - 1)

    def searchLessThanActual(self, new_f_value) -> (Node, InternalBranch):
        for i in reversed(self.TREE):
            for j in i.nodes:
                print(not j.select_to_gr)
                print(not j.was_explored)
                print(j.f_value != 0)
                print(j.f_value < new_f_value)
                if not j.select_to_gr and not j.was_explored and j.f_value < new_f_value:
                    return j, i
        return None, None

    def backtrack(self, back_branch: InternalBranch, back_node: Node):
        self.TREE = self.TREE[:back_branch.father_index + 1]

        for i in self.TREE[back_branch.father_index].nodes:
            if i.select_to_gr:
                i.select_to_gr = False
                i.was_explored = True
            if i == back_node:
                self.TREE[back_branch.father_index].exploring_number = i.number
                i.select_to_gr = True

    def stuck(self) -> (Node, InternalBranch):
        best_node = None
        index = 0
        while best_node is None:
            index -= 1
            less_valor = 10
            for i in self.TREE[index].nodes:
                if not i.select_to_gr and not i.was_explored and i.f_value < less_valor:
                    best_node = i

        return best_node, self.TREE[index]

    def __init__(self):
        pass

    def shouldBeIn(self, valor) -> tuple:
        return self.RIGHT_POSITION[valor]

    def distToRightPlace(self, valor, loc: tuple):
        return dist2points(loc, self.shouldBeIn(valor))

    def getSolucao(self, qc: QuebraCabecaImp):
        count = 0

        while not qc.isOrdenado():
            tab = qc.getTab()
            empty_loc = qc.getPosVazio()

            count += 1

            best_node = None
            best_score = 10

            new_branch = InternalBranch(father_index=len(self.TREE), tab_state=tab)

            print("Init:")
            print(qc.toString())

            for i in qc.getMovePossiveis():
                number = tab[i.getLinha()][i.getColuna()]

                if tab[0] == [1, 2, 3] and tab[0].__contains__(number):
                    continue

                if len(self.TREE) > 0 and self.TREE[-1].exploring_number == number:
                    continue

                node = Node(
                    f=self.distToRightPlace(number, empty_loc.toTuple()),
                    number=number,
                    actual_pos=i.toTuple()
                )

                new_branch.nodes.append(node)

                if 0 <= node.f_value < best_score:
                    best_node = node
                    best_score = node.f_value

            print(' [] '.join(str(e) for e in new_branch.nodes))

            if best_node is None:
                back_node, back_branch = self.stuck()
            else:
                back_node, back_branch = self.searchLessThanActual(best_score)

            if back_node is None:
                best_node.select_to_gr = True
                new_branch.exploring_number = best_node.number
                self.TREE.append(new_branch)
            else:
                self.backtrack(back_branch, back_node)
                best_node = back_node
                qc.setTab(back_branch.tab_state)
                empty_loc = qc.getPosVazio()
                print(f"Back To: {back_branch}")
                print(f"Back To: {back_node}")
                # print(qc.toString())

            print(' || '.join(str(e) for e in self.TREE))

            try:
                qc.move(empty_loc.getLinha(), empty_loc.getColuna(), best_node.actual_pos[0], best_node.actual_pos[1])
            except Exception as ex:
                self.printError(ex, best_node, best_score, qc)
                break

            # print("End:")
            print(qc.toString())
            # print(count)

            if count >= 60:
                print("Algo de errado, não está certo 🤔")
                break

        print("BINGOOOOOOOOOOOOOOOOOOOOOOOOOOOO!!!")
        return []

    @staticmethod
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
