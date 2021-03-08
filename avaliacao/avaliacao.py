import pandas as pd
import timeit

class AvaliacaoAlgoritmo:
    """
    Classe para registrar o resultado das execuções de um algoritmo
    """
    def __init__(self,quantidade_repeticoes,lista_parametros):
        self.quantidade_repeticoes = quantidade_repeticoes
        self.lista_parametros = lista_parametros

    def retorna_resultados(self,funcao,nome_algoritmo):
        data=[]
        for parametro in self.lista_parametros:
            for i in range(self.quantidade_repeticoes):
                starttime = timeit.default_timer()
                custo = funcao(*parametro)
                interval =  timeit.default_timer() - starttime
                data.append([nome_algoritmo,parametro,custo,interval])

        retorno = pd.DataFrame(data=data,columns=['algoritmo','parametro','custo','tempo'])

        return retorno
    def retorna_intervalo_confianca(self):
        pass






