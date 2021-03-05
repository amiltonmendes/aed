from enum import Enum
import numpy as np
class OperacoesPossiveis(Enum):
    NOP = 0
    SWAP = 1
    DELETE = 2
class Movimento:
    def __init__(self,operacao,posicao):
        self.operacao = operacao

        self.posicao = posicao
    def custo(self):
        if self.operacao==OperacoesPossiveis.NOP:
            return 0
        else:
            return 1
class ListaMovimentos:
    def __init__(self, palavrax,palavray,penalidade):
        self.palavrax = palavrax
        self.palavrax_modificada = self.palavrax
        self.palavray = palavray
        self.posicao_palavrax=0
        self.ultima_posicao_palavrax=0
        self.posicao_palavray=0
        self.movimentos = []
        self.custo_total = 0
        self.inicializacao = True
        self.penalidade = penalidade

    def adiciona_movimento(self,operacao):
        if self.permite_operacao(operacao) == False:
            return False
        if operacao == OperacoesPossiveis.NOP:
            movimento = Movimento(operacao, self.ultima_posicao_palavrax)
            self.movimentos.append(movimento)
            if len(self.palavray)<=self.posicao_palavray:
                self.custo_total=np.Infinity
                return False
            #operacao válida?
            if self.palavrax_modificada[self.ultima_posicao_palavrax] == self.palavray[self.posicao_palavray]:
                self.custo_total+=movimento.custo()
            #caracteres diferentes
            else:
                self.custo_total+=np.Infinity
            self.ultima_posicao_palavrax+=1
            self.posicao_palavray+=1
            self.posicao_palavrax=self.ultima_posicao_palavrax
        elif operacao == OperacoesPossiveis.DELETE:
            movimento = Movimento(operacao, self.ultima_posicao_palavrax)
            self.movimentos.append(movimento)
            #tentativa de operação de deleção sem que a palavra 1 tenha mais caracteres que a palavra 2
            if (len(self.palavrax_modificada)) < (len(self.palavray)):
                self.custo_total+=np.Infinity
                return False
            #verificar o próximo elemento está em uma posição válida
            elif (len(self.palavrax_modificada)>=self.posicao_palavrax+1):
                self.palavrax_modificada=delete(self.palavrax_modificada,self.ultima_posicao_palavrax)
                self.custo_total+= movimento.custo()
            else:
                self.custo_total+=np.Infinity
                return False
            #self.ultima_posicao_palavrax
            self.posicao_palavrax=self.ultima_posicao_palavrax

        else:
            #swap
            movimento = Movimento(operacao, self.posicao_palavrax)
            self.movimentos.append(movimento)

            if len(self.palavrax_modificada) > self.posicao_palavrax + 1:
                self.palavrax_modificada=self.swap(self.palavrax_modificada,self.posicao_palavrax)
                self.custo_total+=movimento.custo()
                self.posicao_palavrax+=1

            elif self.posicao_palavrax > self.ultima_posicao_palavrax+1:
                self.posicao_palavrax=self.ultima_posicao_palavrax
                self.palavrax_modificada=self.swap(self.palavrax_modificada,self.posicao_palavrax)
                self.custo_total+=movimento.custo()
                self.posicao_palavrax+=1
                #self.ultima_posicao_palavrax

            else:
                self.custo_total+=np.Infinity
                self.posicao_palavrax+=1
        return True
    def permite_operacao(self,operacao):
        if self.custo_total == np.Infinity:
            return False
        if (operacao == OperacoesPossiveis.DELETE) | (operacao == OperacoesPossiveis.NOP):
            return self.ultima_posicao_palavrax < len(self.palavrax_modificada)
        if operacao == OperacoesPossiveis.SWAP :
            return ((self.posicao_palavrax) >= self.ultima_posicao_palavrax+1) | (self.posicao_palavrax == self.ultima_posicao_palavrax)
    def is_finished(self):
        return (self.palavrax_modificada==self.palavray) & \
               (self.ultima_posicao_palavrax==len(self.palavrax_modificada))


    def swap(self,a, i):
        if len(a) - 1 >= i + 1:
            c = list(a)
            c[i], c[i + 1] = c[i + 1], c[i]
            return ''.join(c)
        #return a

    def delete(self,a, i):
        return a[:i] + a[i + 1:]





def swap(a,i):
    if len(a)-1>=i+1:
        c = list(a)
        c[i],c[i+1] = c[i+1],c[i]
        return ''.join(c)
def delete(a,i):
    return a[:i] + a[i + 1:]


def check(a,b):
    set_a = set(a)
    set_b = set(b)
    any_not_in = lambda a,b : bool(set_a.issuperset(set_b))
    return any_not_in(a,b)
def custo_correction(a,b):
    custo=0
    #tamanho da string a
    na =len(a)
    #tamanho da string b
    nb = len(b)
    #lista de caracteres
    l_a = list(a)
    l_b = list(b)
    #conjunto de caracteres (não repetíveis)
    s_b = set(b)
    #contador da posição da string b
    j=0
    #palavra a após modificação
    a_modified = a
    #contador da palabra a
    i=0
    #contador de laços para tentar inferir complexidade
    contador = 0
    while i <na:
        contador+=1
        #se a posição é igual, incrementa i e não adiciona nada no custo
        if l_a[i] == l_b[j]:
            i+=1
            #caracteres iguais na posição de referência
            j+=1
        else:
            # melhorar essa função de deleção, tendo em vista que podem ocorrer situações
            # em que são deletados caracteres que estão contidos na string b
            # delete
            na -= 1
            a_modified = delete(a_modified, i)
            # i+=1
            custo += 1

            #se forem diferentes, tenta realizar uma operação de swap
            n = 0
            escape = True
            while(escape):
                contador+=1
                #se for existem dois caracteres iguais adjacentes, vai até o último da sequência antes de realizar um swap
                while l_a[i + n + 1] == l_a[i + n]:
                    contador+=1
                    n+=1
                a_modified = swap(a_modified,i+n)
                l_a = list(a_modified)
                custo += 1
                if (l_a[i + n+1] == l_b[i + n+1]) :
                    escape = False
                n+=1
    print (contador)
    return custo

