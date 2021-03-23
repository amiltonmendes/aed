from src.utils.utils_string_corrector import OperacoesPossiveis,ListaMovimentos
import numpy as np
from geneticalgorithm import geneticalgorithm as ga
import editdistance

class AvaliaMovimento:
    def __init__(self,a,b):
        self.stringa=a
        self.stringb=b
    def custo(self,parametros):
        lst = ListaMovimentos(self.stringa,self.stringb,3,True)
        for param in parametros:
            if param == OperacoesPossiveis.NOP.value:
                lst.adiciona_movimento(OperacoesPossiveis.NOP)
            elif param == OperacoesPossiveis.SWAP.value:
                lst.adiciona_movimento(OperacoesPossiveis.SWAP)
            elif param == OperacoesPossiveis.BACK_POS.value:
                lst.adiciona_movimento(OperacoesPossiveis.BACK_POS)
            elif param == OperacoesPossiveis.DELETE.value:
                lst.adiciona_movimento(OperacoesPossiveis.DELETE)
        #if(lst.is_same()==False):
        #    lst.custo_total += lst.penalidade*len(lst.movimentos)

        return (lst.penalidade**(2*editdistance.eval(lst.palavrax_modificada,lst.palavray))-1)\
               +lst.custo_total
    def palavra(self,parametros):
        lst = ListaMovimentos(self.stringa,self.stringb,3,True)
        for param in parametros:
            if param == OperacoesPossiveis.NOP.value:
                lst.adiciona_movimento(OperacoesPossiveis.NOP)
            elif param == OperacoesPossiveis.SWAP.value:
                lst.adiciona_movimento(OperacoesPossiveis.SWAP)
            elif param == OperacoesPossiveis.BACK_POS.value:
                lst.adiciona_movimento(OperacoesPossiveis.BACK_POS)
            elif param == OperacoesPossiveis.DELETE.value:
                lst.adiciona_movimento(OperacoesPossiveis.DELETE)
        return lst.palavrax_modificada

def roda_genetic(a,b,k=0):
    """
    Função proxy para a utilização de algoritmos genéticos para o cálculo do custo
    para a transformação de uma string em outra
    :param a: palavra 1
    :param b: palavra 2
    :return: custo de transformação da string 1 em string 2 segundo o algoritmo genético
    """
    avalia = AvaliaMovimento(a,b)

    total_populacao=3**(max(len(a),len(b)))
    populacao_avaliada = max(total_populacao/2,10)
    interacoes = 3000#max(populacao_avaliada,30)
    if k==0:
        num_parametros = len(a)
    else:
        num_parametros=k
    varbound =  np.array([[0,3]]*num_parametros)
    algorithm_param = {'max_num_iteration': interacoes,\
                       'population_size':populacao_avaliada,\
                       'mutation_probability':0.1,\
                       'elit_ratio': 0.01,\
                       'crossover_probability': 0.7,\
                       'parents_portion': 0.1,\
                       'crossover_type':'uniform',\
                       'max_iteration_without_improv':100}
    model = ga(function=avalia.custo,dimension=num_parametros,variable_type='int',variable_boundaries=varbound\
               ,convergence_curve=False,progress_bar=False,\
               algorithm_parameters=algorithm_param)
    model.run()
    return model
'''a='abacs'
b='caba'

model = distancia_genetic(a,b,13)
print(model.best_function)
variable = model.best_variable
#variable = [1,1,1,3,1,1,3,1,3,0,0,0,0,2]

avaliacao = AvaliaMovimento(a,b)
print(variable)
print(avaliacao.palavra(variable))
print(avaliacao.custo(variable))'''


