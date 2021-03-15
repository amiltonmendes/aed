from enum import Enum
import numpy as np
class OperacoesPossiveis(Enum):
    NOP = 0
    SWAP = 1
    DELETE = 2
    BACK_POS = 3
class Movimento:
    def __init__(self,operacao,posicao):
        self.operacao = operacao

        self.posicao = posicao
    def custo(self):
        if (self.operacao==OperacoesPossiveis.NOP) | (self.operacao == OperacoesPossiveis.BACK_POS):
            return 0
        else:
            return 1
class ListaMovimentos:
    def __str__(self):
        return [movimento.operacao.name for movimento in self.movimentos]
    def __init__(self, palavrax,palavray,penalidade,movimentos_adicionais=False):
        self.palavrax = palavrax
        self.palavrax_modificada = self.palavrax
        self.palavray = palavray
        self.posicao_palavrax=0
        self.ultima_posicao_palavrax=0
        self.posicao_palavray=0
        self.movimentos = []
        self.custo_total = 0
        self.penalidade = penalidade
        self.erro = False
        self.movimentos_adicionais=movimentos_adicionais
    def adiciona_movimento(self,operacao):
        if (self.permite_operacao(operacao) == False) | self.erro:
            self.erro = True
            self.custo_total+=self.penalidade
            return False
        if operacao != OperacoesPossiveis.SWAP:
            # se a última operação for um swap
            if self.ultima_posicao_palavrax!=self.posicao_palavrax:
                #se a palavray tem comprimento que permite fazer a comparação
                if len(self.palavray) > self.posicao_palavrax:
                    #se os caracteres na posição final do último swap são iguais, então foi um movimento válido
                    if self.palavrax_modificada[self.posicao_palavrax] != self.palavray[self.posicao_palavrax]:
                        self.custo_total+=self.penalidade
                else:
                    self.custo_total+=self.penalidade


        if operacao == OperacoesPossiveis.BACK_POS:
            movimento = Movimento(operacao,self.posicao_palavrax)
            self.posicao_palavrax=self.ultima_posicao_palavrax
            self.movimentos.append((movimento))
            return True
        elif operacao == OperacoesPossiveis.NOP:
            movimento = Movimento(operacao, self.ultima_posicao_palavrax)
            self.movimentos.append(movimento)
            #se estiver na última posição, e houver a possibilidade de se ter operações redundantes no final
            if self.movimentos_adicionais & ((len(self.palavrax_modificada)==self.ultima_posicao_palavrax+1) \
                                             & (len(self.palavray)==self.posicao_palavray+1)):
                if (self.palavrax_modificada[-1] == self.palavray[-1]) :
                    return True
                elif (self.palavrax_modificada[-1] != self.palavray[-1]) :
                    self.custo_total+=self.penalidade
                    self.erro=True
                    return False
            if len(self.palavray)<=self.posicao_palavray:
                self.custo_total+=self.penalidade#np.Infinity
                self.erro = True
                return False
            #operacao válida?
            if self.palavrax_modificada[self.ultima_posicao_palavrax] == self.palavray[self.posicao_palavray]:
                self.custo_total+=movimento.custo()
            #caracteres diferentes
            else:
                self.custo_total+=self.penalidade#np.Infinity
                self.erro=True
                return False
            self.ultima_posicao_palavrax+=1
            self.posicao_palavray+=1
            self.posicao_palavrax=self.ultima_posicao_palavrax
            return True
        elif operacao == OperacoesPossiveis.DELETE:
            movimento = Movimento(operacao, self.ultima_posicao_palavrax)
            self.movimentos.append(movimento)
            #tentativa de operação de deleção sem que a palavra 1 tenha mais caracteres que a palavra 2
            if (len(self.palavrax_modificada)) <= (len(self.palavray)):
                self.custo_total+=self.penalidade#np.Infinity
                self.erro=True
                return False
            #verificar o próximo elemento está em uma posição válida
            elif (len(self.palavrax_modificada)>=self.posicao_palavrax+1):
                self.palavrax_modificada=self.delete(self.palavrax_modificada,self.ultima_posicao_palavrax)
                self.custo_total+= movimento.custo()
            else:
                self.custo_total+=self.penalidade#np.Infinity
                self.erro=True
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
            else:
                self.custo_total+=self.penalidade#np.Infinity
                self.erro=True
                self.posicao_palavrax+=1
                return False
        return True
    def permite_operacao(self,operacao):
        #if self.custo_total == np.Infinity:
        if self.erro == True:
            self.custo_total+=self.penalidade
            self.erro=True
            return False
        if (operacao == OperacoesPossiveis.DELETE) :
            return self.ultima_posicao_palavrax < len(self.palavrax_modificada)
        if ( operacao == OperacoesPossiveis.BACK_POS):
            return self.posicao_palavrax != self.ultima_posicao_palavrax
        if (operacao == OperacoesPossiveis.NOP) :
            if self.movimentos_adicionais:
                if self.ultima_posicao_palavrax == len(self.palavrax_modificada):
                    return True
            return self.ultima_posicao_palavrax < len(self.palavrax_modificada)
        if operacao == OperacoesPossiveis.SWAP :
          return (len(self.palavrax_modificada)>self.posicao_palavrax+1)
    def is_finished(self):
        return (self.ultima_posicao_palavrax>=len(self.palavrax_modificada))
    def is_same(self):
        return self.palavrax_modificada == self.palavray
    def penaliza(self):
        self.custo_total+=np.Infinity



    def swap(self,a, i):
        if len(a) - 1 >= i + 1:
            c = list(a)
            c[i], c[i + 1] = c[i + 1], c[i]
            return ''.join(c)
    def delete(self,a, i):
        return a[:i] + a[i + 1:]

'''def swap(a,i):
    if len(a)-1>=i+1:
        c = list(a)
        c[i],c[i+1] = c[i+1],c[i]
        return ''.join(c)
def delete(a,i):
    return a[:i] + a[i + 1:]'''


