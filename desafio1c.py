# A função recebe um símbolo e monta o autômato base para aquele símbolo

count_i = 0     # Contador usado para gerar os nomes dos estados

def er2afn_base(simbolo):
    global count_i
    count_i += 1
    if simbolo == None:  #  representa o vazio
        QSet = {f'i{count_i}', f'f{count_i}'}
        Sigma = {}
        Delta = {}
        FSet = {f'f{count_i}'}
        return (QSet, Sigma, Delta, f'i{count_i}', FSet)

    elif simbolo == '':  # '' representa o epilson
        QSet = {f'i{count_i}', f'f{count_i}'}
        Sigma = {}
        Delta = { (f'i{count_i}', ''):{f'f{count_i}'} }
        FSet = {f'f{count_i}'}
        return (QSet, Sigma, Delta, f'i{count_i}', FSet)
    else:       # {a} representa o epilson
        QSet = {f'i{count_i}', f'f{count_i}'}
        Sigma = {simbolo}
        Delta = {(f'i{count_i}', simbolo):{f'f{count_i}'}}
        FSet = {f'f{count_i}'}
    return (QSet, Sigma, Delta, f'i{count_i}', FSet)

# Transformação ER para AFN (2)

#A funcao é baseada em  2 automatos R e S, usando o padrão (QSet, Sigma, Delta, EstadoInicial, FSet)

def er2afn_union(R, S):
    global count_i

    count_i += 1
    new_i = f'i{count_i}'
    new_f = f'f{count_i}'

    newQSet = R[0].union(S[0]).union({new_i, new_f})
    newSigma = R[1].union(S[1])

    end_R = next(iter(R[4]))
    end_S = next(iter(S[4]))

    newDelta = {
        (new_i, ''):{R[3], S[3]},
        (end_R, ''):{new_f},
        (end_S, ''):{new_f},
        **R[2],
        **S[2]
    }
    newFSet = {new_f}
    return (newQSet, newSigma, newDelta, new_i, newFSet)

#A funcao é baseada em  2 automatos R e S, usando o padrão (QSet, Sigma, Delta, EstadoInicial, FSet)

def er2afn_concat(R, S):
    newQSet = R[0].union(S[0])
    newSigma = R[1].union(S[1])

    end_R = next(iter(R[4]))

    newDelta = {
        **R[2],
        (end_R, ''): {S[3]},
        **S[2]
    }
    newFSet = S[4]
    return (newQSet, newSigma, newDelta, R[3], newFSet)
#A funcao é baseada em  2 automatos R e S, usando o padrão (QSet, Sigma, Delta, EstadoInicial, FSet)
#

def er2afn_kleene(R):
    global count_i

    count_i += 1
    new_i = f'i{count_i}'
    new_f = f'f{count_i}'

    newQSet = R[0].union({new_i, new_f})
    newSigma = R[1]

    end_R = next(iter(R[4]))

    newDelta = {
        (new_i, ''):{R[3], new_f},
        (end_R, ''):{new_f, R[3]},
        **R[2]
    }
    newFSet = {new_f}

    return (newQSet, newSigma, newDelta, new_i, newFSet)

# 14 - Transformacao ER para AFN (5)

def er2afn(expreg):
    operador = expreg[0]                            # Obtem o primeiro operador

    operando_1 = expreg[1]                          # Obtem o primeiro parametro, que pode ser um operando
                                                    # ou uma outra expressão regular (ER)
    if type(operando_1) is tuple:                   
        operando_1 = er2afn(operando_1)             # Caso seja uma outra ER, chama a função recursivamente
    else:
        operando_1 = er2afn_base(operando_1)        # Caso não, busca o automato base para o simbolo

    if len(expreg) > 2:                             # Como o segundo parâmetro é opcional, é preciso saber
        operando_2 = expreg[2]                      # se ele existe antes de buscar seu valr
        if type(operando_2) is tuple:
            operando_2 = er2afn(operando_2)
        else:
             operando_2 = er2afn_base(operando_2)
    if operador == '+':                             # Para cada operador a função correspondente é chamada
        return er2afn_union(operando_1, operando_2)
    elif operador == '':
        return er2afn_concat(operando_1, operando_2)
    elif operador == '*':
        return er2afn_kleene(operando_1)
#Autômato Finito Não Determinístico (AFN)

# 2 - delta do AFN
def delta(automato, estado, simbolo):
    try:
        return automato[2][(estado, simbolo)]
    except:
        return {None} 
# o retorno é uma lista de estados
# passando referencia da lista ao inves de valor string. A diferença no AFN ocorre  quando ele esta entrando no estado (o que ainda nao é esse parte)
# 3 - Fecho-Epsilon
# A função eclose pode receber um estado com apenas um elemento (Set1 = 'a') ou um conjunto de elementos (Set2 = 'a','b','c','d').
def eclose(automato,estados):
    if estados == {None}:
        return {}

    simbolo = ''   # O simbolo possui valor '' para definir como se fosse um épsilon.
    eclosure = set()   # Nesta linha foi criado um set vazio eclosure = { }

    for estado in estados:   # Este for serve para percorrer cada estado presente no Set de entrada(estado), seja eles Set1 ou Set2, por exemplo.
        eclosure = eclosure.union({estado}) # usando a definição: q ∈ ECLOSE(q)
        if(delta(automato,estado,simbolo) != {None}): #  Consertando problema quando não existe nenhuma transição vazia no Autômato
            eclosure = eclosure.union(delta(automato, estado, simbolo))  # Nesta linha o eclosure está utilizando o .union para somar o eclose de cada elemento do set de entrada e guardar na própria variável.
            eclosure = eclosure.union(eclose(automato, delta(automato, estado, simbolo)))  # Nesta linha o eclosure está utilizando o .union para somar o eclose de cada elemento do set de entrada e guardar na própria variável.
    return eclosure # Será retornado um Set com o resultado da soma do eclose de cada Set de entrada.
# 4 - Delta estendido do AFN
def delta_hat(automato, estado, palavra):
    if palavra == []:
        return estado
    else:
        palavra_copy = palavra.copy()
        simbolo = palavra_copy.pop()
        fe = eclose(automato, estado)
        fn = set()
        for e in fe:
            estados = delta_hat(automato, {e}, palavra_copy)
            deltas = [delta(automato, estado, simbolo) for estado in estados]
            fn = fn.union(*deltas)
        fn_copy = fn.copy()
        
        for f in fn_copy:
            if f is not None:
                fn = fn.union(eclose(automato, {f}))
        # print("Estados finais", fn)
        return fn
#Assim como no AFD a função vai partir do estado inicial recebido e recursivamente chamar a função delta() até o fim da palavra. Porém no AFN deverá calcular o fecho epsilon (fe)
#para cada estado e posteriormente chamar a função delta() para cada um dos estados preenchendo o vetor de estados encontrados (fn).
# 5 - Função aceitação
def aceita(automato, palavra): # palavra é um array com os simbolos. e.g. [1, 0, 1]
    estados_finais = delta_hat(automato, {automato[3]}, palavra)
    for estado in estados_finais:
        if estado in automato[4]:
            return True
    return  False


a = er2afn(('+', ('*', 1), ('*', 1))) # 1*+1*
b = er2afn(('+', ('*', 1), ('*', 0)))
c = er2afn(('', 0, ('*', 1)))

# == True == #
print(aceita(a, [1,1]))
print(aceita(a, [1]))
print(aceita(a, [1,1,1]))
print(aceita(b, [0,0]))
print(aceita(b, [1,1]))
print(aceita(b, [0]))
print(aceita(c, [0,1,1]))
print(aceita(c, [0,1,1,1,1]))
print(aceita(c, [0,1]))
print(aceita(c, [0]))

print()

# == False == #
print(aceita(a, []))
print(aceita(a, [0,0,1]))
print(aceita(a, [1,1,0]))
print(aceita(b, [1,0]))
print(aceita(b, [1,1,0,0]))
print(aceita(a, [1,0,1,0]))
print(aceita(c, [1,0]))
print(aceita(c, [1,0,1,1]))
print(aceita(c, [1,1,1,1]))
print(aceita(c, [0,0,1]))
