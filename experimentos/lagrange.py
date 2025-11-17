import numpy as np
import matplotlib.pyplot as plt
# Pra plotar os gráficos
import yfinance as yf
# Pra usar o banco de dados
from datetime import datetime, timedelta
# Pra saber qual a hora que o usuário está usando o programa

def interpolacaoDeLagrange(X, Y, xAlvo):
    n = len(X)
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

    # Ações famosas da B3 (Sugeridas pela IA)
    acoes = {
        1: ("PETR4", "PETR4.SA"),
        2: ("VALE3", "VALE3.SA"),
        3: ("ITUB4", "ITUB4.SA"),
        4: ("B3SA3", "B3SA3.SA"),
        5: ("BBAS3", "BBAS3.SA")
    }

    print("\nEscolha uma ação:")
    for k, v in acoes.items():
        print(f"{k} - {v[0]}")
    # Printa o primeiro valor de cada índice da tupla "ações"

    escolha = int(input("Número da ação: "))
    nome, ticker = acoes[escolha]

    print(f"\nObtendo dados reais da {nome} hoje\n")

    # Carregar dados das últimas 24h com intervalo de 1h
    dados = yf.download(
        tickers=ticker,
        period="1d",
        interval="1h"
    )

    # Garantir que só pegaremos horas que já aconteceram
    dados = dados[["Close"]].dropna()

    # Pegar as últimas 5 horas
    dados = dados.tail(5)

    # Criar X (horas reais) e Y (preços)
    X = dados.index.hour.tolist()
    Y = dados["Close"].tolist()

    print("\nPontos usados para interpolação:")
    for x, y in zip(X, Y):
        print(f"{x}h - R${y:.2f}")

    # xAlvo digitado pelo usuário
    xAlvo = float(input("\nDigite uma hora para interpolar: "))
    yAlvo = interpolacaoDeLagrange(X, Y, xAlvo)

    print(f"\nValor interpolado em x = {xAlvo}: y = R${yAlvo:.4f}")

    xPlot = np.linspace(min(X), max(X), 200)
    yPlot = [interpolacaoDeLagrange(X, Y, x) for x in xPlot]

    plt.figure(figsize=(10, 6))
    plt.plot(X, Y, 'ro', label='Pontos reais (últimas 5 horas)')
    plt.plot(xPlot, yPlot, 'b-', label='Interpolação de Lagrange')
    plt.plot(xAlvo, yAlvo, 'gs', markersize=8, label='Ponto interpolado')

    plt.title(f"Interpolação de Lagrange para {nome}")
    plt.xlabel("Hora do dia")
    plt.ylabel("Preço (R$)")
    plt.grid()
    plt.legend()
    plt.show()
