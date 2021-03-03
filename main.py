def swap(a,i):
    if len(a)-1>=i+1:
        c = list(a)
        c[i],c[i+1] = c[i+1],c[i]
        return ''.join(c)
    raise IndexError
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
        #se existe o caractere no conjunto de caracteres de b
        if s_b.__contains__(l_a[i]):
            #se a posição é igual, incrementa i e não adiciona nada no custo
            if l_a[i] == l_b[j]:
                i+=1
                #caracteres iguais na posição de referência
                j+=1
            else:
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
        #melhorar essa função de deleção, tendo em vista que podem ocorrer situações
        # em que são deletados caracteres que estão contidos na string b
        else:
            #delete
            na-=1
            a_modified=delete(a_modified,i)
            #i+=1
            custo+=1
    print (contador)
    return custo

if __name__ == '__main__':
    a = 'bacaxis'
    b=  'ixacab'
    print(custo_correction(a,b))