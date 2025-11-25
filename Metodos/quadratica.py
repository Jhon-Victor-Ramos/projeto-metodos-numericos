import numpy as np

def interpolacaoQuadratica(x, y, xAlvo):
    # Montagem da Matriz A (Matriz de Vandermonde para grau 2)
    # Coluna 0: x^2, Coluna 1: x^1, Coluna 2: 1 (ou x^0)
    A = np.array([
        [x[0]**2, x[0], 1],
        [x[1]**2, x[1], 1],
        [x[2]**2, x[2], 1]
    ])

    # Montagem do Vetor B (Os preços conhecidos)
    B = np.array(y)

    # Resolução do Sistema Linear (Encontrar a, b, c)
    try:
        coeficientes = np.linalg.solve(A, B)
    except np.linalg.LinAlgError:
        print("Impossível resolver o sistema.")
        return 0.0

    a = coeficientes[0]
    b = coeficientes[1]
    c = coeficientes[2]

    # Cálculo do Resultado Final: P(xAlvo) = a*x^2 + b*x + c
    resultado = a * (xAlvo**2) + b * xAlvo + c
    
    return resultado