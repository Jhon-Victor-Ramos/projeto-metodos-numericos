import numpy as np
import matplotlib.pyplot as plt

def coeficientes(x, y):
    n = len(x)
    ordemAnterior = y.copy()
    ordemAtual = [0] * n
    coeficientes = [ordemAnterior[0]]
    for ordem in range(1, n):
        for i in range(n - ordem):
            ordemAtual[i] = (ordemAnterior[i + 1] - ordemAnterior[i]) / (x[i + ordem] - x[i])
        coeficientes.append(ordemAtual[0])
        ordemAnterior = ordemAtual.copy()
        ordemAtual = [0] * (n - ordem)
    return coeficientes

def interpoladorDiferencasDivididas(x, y, xAlvo):
    coefs = coeficientes(x, y)
    n = len(coefs)
    resultado = coefs[0]
    produto = 1.0
    for i in range(1, n):
        produto *= (xAlvo - x[i - 1])
        resultado += coefs[i] * produto
    return resultado
