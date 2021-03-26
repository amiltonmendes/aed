import pandas
from timeit import default_timer as timer
import pandas as pd
import timeit


class AvaliacaoAlgoritmo:
    """
    Classe para registrar o resultado das execuções de um algoritmo
    """
    def __init__(self, quantidade_repeticoes, lista_parametros):
        self.quantidade_repeticoes = quantidade_repeticoes
        self.lista_parametros = lista_parametros

    def retorna_resultados(self, funcao, nome_algoritmo):
        data = []
        iteracoes = 0
        for index, row in self.lista_parametros.iterrows():
        #for parametro in self.lista_parametros:
            for i in range(self.quantidade_repeticoes):
                starttime = timeit.default_timer()
                #custo = funcao(*parametro)
                # iteracoes = funcao(list(row['Origem']), list(row['Destino']), self.quantidade_repeticoes, 0)
                #Unix  xi
                iteracoes = funcao(list('Unix'), list('xi'), self.quantidade_repeticoes, 0)
                
                interval =  timeit.default_timer() - starttime
                #data.append([nome_algoritmo, parametro, custo, interval])
                data.append([nome_algoritmo, row['Origem'], row['Destino'], iteracoes, interval])

        #retorno = pd.DataFrame(data=data, columns=['algoritmo', 'parametro', 'custo', 'tempo'])
        retorno = pd.DataFrame(data=data, columns=['algoritmo', 'Origem', 'Destino', 'custo', 'tempo'])

        return retorno
    def retorna_intervalo_confianca(self):
        pass
class LeeAlgorithm:
    def __init__(self,interacoes):
        self.interacoes=interacoes
    def roda_lee(self,a,b):
        return s2s(list(a),list(b),self.interacoes,0)

Alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def doTroca(X, posicao):
    X[posicao - 1], X[posicao] = X[posicao], X[posicao - 1]
    return X

def doDelete(Origem, Destino, k, iteracoes):
    for letra in range(Destino):
        i = Origem.find(letra)
        for j in range(i - 1):
            Origem.pop(0)
            iteracoes += 1
        k = k - (i - 1)
        Destino.pop(0)
        Origem.pop(0)
    if len(Origem) > 0:
        for i in len(Origem):
            Origem.pop(0)
            iteracoes += 1
        k = k - len(Origem)

def doSwap(Origem, Destino, k, iteracoes):
    # Verifica se só swap já resolve
    if len(Origem) == 0:
        return iteracoes
    i = ''.join(Origem).find(Destino[0])
    icpy = i
    while (i - 1 <= k):
        if i > 1:
            for j in range(i - 1):
                Origem = doTroca(Origem, icpy - 1)
                icpy -= 1
                iteracoes += 1
            k = k - (i -1)
        Origem.pop(0)
        Destino.pop(0)
        if len(Origem) > 0:
            i = ''.join(Origem).find(Destino[0])
            icpy = i
        else:
            #print ('Swap Only')
            return iteracoes
    return -1

# Préprocessamento
def s2s(Origem, Destino, k, iteracoes):
    #print (''.join(Origem) + ' > ' + ''.join(Destino) + ' > ' + str(k))
    iteracoes += 1
    if (len(Origem) == 0 or len(Destino) == 0):
        return iteracoes
    # Verifica se é um NPCompleto (YES-Instance / NO-Instance)
    # 1 - O número de iterações não pode ser negativo 
    # O(1)
    if k < 0:          
        #print ('Tamanho k inválido')
        return -1
    
    # 2 - deve haver número de edições iguais (pelo menos) a soma dos tamanhos
    # O(1)
    if (len(Origem) - len(Destino)) > k:   
        #print ('Origem - Destino > k')
        return -1

    # 3 - Destino tem q ser maior
    # O(1)
    if len(Origem) < len(Destino):         
        #print ('Origem < Destino')
        return -1
    
    # 4 - Se há número suficientes de ocorrências
    # O(m)
    for letra in Alfabeto:           
        if Origem.count(letra) < Destino.count(letra):
            #print ('Letra inexistente')
            return -1
    
    # 5 - iterativo - remove a primeira letra
    # O (k + m)
    if (Origem[0] == Destino[0]):               # 
        Origem.pop(0)
        Destino.pop(0)
        return s2s(Origem, Destino, k, iteracoes)
    
    # 6 - Se destino está contido no origem (supersequencia)
    # O (k + m)
    if ''.join(Destino).find(''.join(Origem)) > 0:
        if len(Origem) - len(Destino) <= k: #####if len(Origem) - len(Destino) > k:
            return doDelete(Destino, Origem, k, iteracoes)
        else:
            return -1;

    # 7 - Se somente Swap resolve
    # O(k + m)
    if len(Destino) == len(Origem):             # só precisa de S se tem o mesmo tamanho e letras
        for letra in Destino:
            if Origem.count(letra) != Destino.count(letra):
                return -1
        return doSwap(Origem, Destino, k, iteracoes)
    
    #8
    tmpOrigem = Origem[:]
    tmpOrigem.pop(0)
    testeiteracoes = s2s(tmpOrigem, Destino, k-1, iteracoes)
    if testeiteracoes > 0:
        return testeiteracoes;
    Origem = doTroca(Origem, 0)
    return s2s(Origem, Destino, k-1, iteracoes)

##################### para teste com valores fixos 
#sOrigem = list('abacaxi')
#sDestino = list('ixacaba')

#sOrigem = list('afeabsesec')
#sDestino = list('abce')

#gControle = ["suas", "massa", "fruta", "tudo", "pilha", "fogo", "grupo", "cha", "abacaxi", "exato"]
#Dicionario = open("DicionarioBruto.txt",'r')
#fbOut = open("outCanada.csv",'w')
#fbMassa = open("DicionarioNPCompleto.csv",'w')

#print ("Comecei")
#for palavra in Dicionario:
#    palavra = palavra.replace("\n", "") # Remove a queblra de lina (\n) do final da linha
#    gControle = open("DicionarioBruto2.txt",'r')
#    for Controle in gControle:
#        Controle = Controle.replace("\n", "") # Remove a queblra de lina (\n) do final da linha
#        inicio = timer() #time.time()
#        iteracoes = 0
#        isFC = s2s(list(palavra), list(Controle), 20, iteracoes)
#        fim = timer() #time.time()
#        fbOut.write(palavra + ";" + Controle + ";" + str(iteracoes) + ";" + str(inicio) + ";" + str(fim) + "\n")
 
#        if (isFC > 0 and palavra != Controle):
#            fbMassa.write(palavra + ";" + Controle + ";" + str(iteracoes) + "\n")
#        print (palavra + ' > ' + Controle + ' > ' + str(isFC))
#    gControle.close()
    
#print ("Acabei !")
#Dicionario.close()
#fbOut.close()

############### Para testes com entrada em batch
'''dEntrada = pandas.read_csv('../../../npcompleto.csv', names=['Origem', 'Destino']) #, chunksize=1), usecols=[1,2]
dEntrada = dEntrada.head(1)   # Para limitar o tamanho do teste
avaliacao_genetico = AvaliacaoAlgoritmo(30, dEntrada[['Origem', 'Destino']])

df = avaliacao_genetico.retorna_resultados(s2s, 'lee')
df.to_csv('resultados_Exato_out.csv')
print ('Acabei')'''