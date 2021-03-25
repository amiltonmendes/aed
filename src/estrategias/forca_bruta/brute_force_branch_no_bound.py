import pybnb
from src.utils.utils_string_corrector import OperacoesPossiveis,ListaMovimentos
from copy import deepcopy
import math

class Simple(pybnb.Problem):
    '''
    Classe com a implementação dos métodos branch and bound do pacote pybnb
    desenvolvida para adequar a heurística branch and bound ao problema
    String to string correction SR20
    '''
    def __init__(self,str1,str2):

        self._xL, self._xU = -len(str1)**len(str1), len(str1)**len(str1)+1
        self.lst = ListaMovimentos(str1, str2, 3)
        self.custo=len(str1)**len(str1)
        self.max_operacoes = math.factorial(len(str1))

    #
    # required methods
    #
    def sense(self):
        return pybnb.minimize
    def objective(self):
        return self.custo
    def bound(self):
        return self.custo-1
    def save_state(self, node):
        node.state = (self.lst,self._xL, self._xU, self.custo)
    def load_state(self, node):
        (self.lst,self._xL, self._xU, self.custo)= node.state
    def branch(self):
        for i in [OperacoesPossiveis.SWAP,OperacoesPossiveis.DELETE,OperacoesPossiveis.NOP,OperacoesPossiveis.BACK_POS]:
            if (self.lst.custo_total) <= self.max_operacoes:
                p = len(self.lst.movimentos)
                lst_cp = deepcopy(self.lst)
                if lst_cp.adiciona_movimento(i):
                    child = pybnb.Node()
                    if(lst_cp.is_finished()):
                        if self.custo > lst_cp.custo_total:
                            lista_ops = Singleton()
                            if lista_ops.lst == None:
                                lista_ops.lst=lst_cp
                            elif lst_cp.custo_total<lista_ops.lst.custo_total:
                                lista_ops.lst = lst_cp
                    child.state = (lst_cp,self._xL,self._xU,self.custo)
                    yield child
                else:
                    lst_cp.movimentos.clear()
                    lst_cp.movimentos=None
                    lst_cp=None

            else:
                pass
    def notify_solve_finished(self,
                              comm,
                              worker_comm,
                              results):


        print('Resultado: ')
        lst = Singleton().lst
        if lst!= None:
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

def roda_brute(string_a,string_b):
    sng = Singleton()
    sng.lst = None
    problem = Simple(string_a, string_b)
    solver = pybnb.Solver(comm=None)
    results = solver.solve(problem)
    return results.objective

#a='ovas'
#b='avo'

#print(roda_brute(a,b))
'''print(results.objective)
print(results.wall_time)
print(results.solution_status)
'''
