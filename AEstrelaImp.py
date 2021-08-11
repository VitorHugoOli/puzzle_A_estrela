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
    def __init__(self, father_index, f):
        self.select_to_gr: bool = False
        self.father = father_index
        self.was_explored = False
        self.f_value = f


class InteranalBranch():
    nodes: List[Node]


class AEstrelaImp(AEstrela):
    TREE = []
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

    def searchLessThanActual(self, actual_node: Node, index):
        if index == -1:
            return None

        for i in self.TREE[index]:
            if not i.select_to_gr and not i.was_explored and i.f_value < actual_node.f_value:
                return i
        return self.searchLessThanActual(actual_node, index - 1)

    def backtrack(self, node_to_back: Node):
        self.TREE = self.TREE[:node_to_back.father + 1]
        for i in self.TREE[:node_to_back.father + 1]:
            if i.select_to_gr:
                i.select_to_gr = False
                i.was_explored = True
            if i == node_to_back:
                i.select_to_gr = True

    def __init__(self):
        pass

    def shouldBeIn(self, valor) -> tuple:
        return self.RIGHT_POSITION[valor]

    def distToRightPlace(self, valor, loc: tuple):
        return dist2points(loc, self.shouldBeIn(valor))

    def getSolucao(self, qc: QuebraCabecaImp):
        count = 0
        block_last_value = -1

        while not qc.isOrdenado():
            count += 1
            tab = qc.getTab()
            empty_loc = qc.getPosVazio()
            near_dist = ()
            near_dist_score = 10
            sub_nodes = []
            father_index = len(self.TREE) - 1
            index_sub_node = -1

            for i in qc.getMovePossiveis():
                if block_last_value != tab[i.getLinha()][i.getColuna()]:
                    f = self.distToRightPlace(tab[i.getLinha()][i.getColuna()], i.toTuple())

                    sub_nodes.append(Node(father_index, f))

                    if 0 < f < near_dist_score:
                        near_dist = i.toTuple()
                        near_dist_score = f
                        index_sub_node = len(sub_nodes) - 1

            if near_dist == ():
                print("NÃO FOI POSSIVEL MELHORAR")
                break

            result = self.searchLessThanActual(sub_nodes[index_sub_node], len(self.TREE) - 1)

            if result is None:
                self.TREE.append(sub_nodes)
                block_last_value = tab[near_dist[0]][near_dist[1]]
            else:
                self.backtrack(result)

            try:
                qc.move(empty_loc.getLinha(), empty_loc.getColuna(), near_dist[0], near_dist[1])
            except Exception as ex:
                self.printError(ex, near_dist, near_dist_score, qc)
                break

            time.sleep(0.8)
            print(qc.toString())

            if count >= 1000000:
                print("Algo de errado, não está certo 🤔")
                break
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
# ║stack: {traceback.format_exc()}
║Nearst_dist: {near_dist}
║Nearst_dist_score: {near_dist_score}
╚════════════════════════════\u001b[0m
""")
