import pybnb
from utils_string_corrector import OperacoesPossiveis,ListaMovimentos
import numpy as np
from copy import deepcopy, copy
class Simple(pybnb.Problem):
    def __init__(self,str1,str2):

        self._xL, self._xU = -len(str1)**len(str1), len(str1)**len(str1)+1
        self.lst = ListaMovimentos(str1, str2, 0)
        self.custo=len(str1)**len(str1)

    #
    # required methods
    #
    def sense(self):
        return pybnb.minimize
    def objective(self):
        return self.custo #self.lst.custo_total
        #return self.custo#round(self._xU-self._xL,3)
    def bound(self):
        #return -(self.lst.custo_total)**2
        return self.custo-1#-(self._xU - self._xL)**2
    def save_state(self, node):
        node.state = (self.lst,self._xL, self._xU, self.custo)
    def load_state(self, node):
        #(self._xL, self._xU)
        (self.lst,self._xL, self._xU, self.custo)= node.state
    def branch(self):
        #xL, xU = self._xL, self._xU
        #xM = 0.5 * (xL + xU)
        #operacoes
        for i in [OperacoesPossiveis.SWAP,OperacoesPossiveis.DELETE,OperacoesPossiveis.NOP]:
            child = pybnb.Node()
            lst_cp = deepcopy(self.lst)

            if lst_cp.adiciona_movimento(i):
                if(lst_cp.is_finished()):
                    if self.custo > lst_cp.custo_total:
                        self._xU = lst_cp.custo_total
                        self._xL = -1
                        self.custo = lst_cp.custo_total
                        lista_ops = Singleton()
                        if lista_ops.lst == None:
                            lista_ops.lst=lst_cp
                        elif lst_cp.custo_total<lista_ops.lst.custo_total:
                            lista_ops.lst = lst_cp



                child.state = (lst_cp,self._xL,self._xU,self.custo)
                yield child

    def notify_solve_finished(self,
                              comm,
                              worker_comm,
                              results):
        print('Resultado: ')
        lst = Singleton().lst
        print(lst.custo_total)
        print(lst.palavrax_modificada)
        for i in lst.movimentos:
            print(i.operacao.name+' ',end='')

class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.lst=None
        return cls._instance


a='abacaixs'
b='abacaxi'
problem = Simple(a,b)
solver = pybnb.Solver(comm=None)
results = solver.solve(problem)