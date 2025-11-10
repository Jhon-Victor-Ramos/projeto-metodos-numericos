import numpy as np
import matplotlib.pyplot as plt

def interpolacaoDeLagrange(X, Y, xAlvo):
    n = len(X)
    # Já retorna - 1
    resultado = 0.0
    for k in range(n):
        numerador = 1.0
        denominador = 1.0
        for i in range(n):
            if i != k:
                numerador *= (xAlvo - X[i])
                denominador *= (X[k] - X[i])
        lK = numerador / denominador
        resultado += Y[k] * lK
    return resultado

if __name__ == "__main__":
    # Pontos de dados
    X = input("Digite os valores de X separados por espaço: ")
    Y = input("Digite os valores de Y separados por espaço: ")
    X = np.array([float(x) for x in X.split()])
    Y = np.array([float(y) for y in Y.split()])

    # Ponto alvo para interpolação
    xAlvo = float(input("Digite o valor de x para interpolar: "))
    yAlvo = interpolacaoDeLagrange(X, Y, xAlvo)
    print(f"Valor interpolado em x = {xAlvo}: y = {yAlvo}")

    # Visualização
    xPlot = np.linspace(min(X), max(X), 100)
    yPlot = [interpolacaoDeLagrange(X, Y, x) for x in xPlot]

    plt.plot(X, Y, 'ro', label='Pontos de dados')
    plt.plot(xPlot, yPlot, 'red', label='Interpolação de Lagrange')
    plt.plot(xAlvo, yAlvo, 'bo', label='Ponto alvo')
    plt.title('Interpolação de Lagrange')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid()
    plt.show()
