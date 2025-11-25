import numpy as np
import matplotlib.pyplot as plt

def coeficientes(x, y):
    
    n = len(x)
    # A primeira coluna da tabela de diferenças é o próprio y
    ordemAnterior = y.copy()
    # Vetor temporário para armazenar cálculos da ordem atual
    ordemAtual = [0] * n

    # Lista final dos coeficientes (primeiro coeficiente é sempre y[0])
    coeficientes = [ordemAnterior[0]]

    # Loop para construir as diferenças divididas de ordem crescente
    for ordem in range(1, n):
        # Calcula os termos da ordem atual usando a fórmula:
        for i in range(n - ordem):
            ordemAtual[i] = (ordemAnterior[i + 1] - ordemAnterior[i]) / (x[i + ordem] - x[i])

        # O primeiro termo de cada ordem é o coeficiente da forma de Newton
        coeficientes.append(ordemAtual[0])
        # Atualiza vetor da ordem anterior para a próxima iteração
        ordemAnterior = ordemAtual.copy()
        # Ajusta o tamanho do vetor para próxima ordem
        ordemAtual = [0] * (n - ordem)

    return coeficientes



def interpoladorDiferencasDivididas(x, y, xAlvo):
    # Obtém os coeficientes calculados pelas diferenças divididas
    coefs = coeficientes(x, y)
    n = len(coefs)

    # Primeiro termo do polinômio é o primeiro coeficiente
    resultado = coefs[0]
    # Termo acumulador para (x - x0), (x - x0)(x - x1), ...
    produto = 1.0

    # Monta o polinômio incrementalmente usando a forma de Newton
    for i in range(1, n):
        produto *= (xAlvo - x[i - 1])
        resultado += coefs[i] * produto

    return resultado
