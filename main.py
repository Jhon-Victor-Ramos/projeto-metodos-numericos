import matplotlib
# Mantendo o modo 'Agg' para evitar erros no Linux
matplotlib.use('Agg') 

import yfinance as yf
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Importando os módulos da pasta Métodos
from Metodos.diferencasDivididas import interpoladorDiferencasDivididas
from Metodos.quadratica import interpolacaoQuadratica

def main():
    print("\nInterpolação de Preços de Ações no dia 19/11/2025\n")
    
    acoes = {
        '1': 'PETR4.SA',
        '2': 'VALE3.SA', 
        '3': 'ITUB4.SA', 
        '4': 'BBDC4.SA',
        '5': 'BBAS3.SA'
    }

    for k, v in acoes.items():
        print(f"{k} - {v}")
    
    escolha_acao = input("Escolha uma ação: ")
    ticker = acoes.get(escolha_acao)

    if not ticker:
        print("Opção inválida.")
        return

    # Obtendo os dados da ação selecionada de 5 em 5 minutos
    print(f"Baixando dados de {ticker}...")
    dados_gerais = yf.download(ticker, start="2025-11-19", end="2025-11-20", interval="5m", progress=False)

    if dados_gerais.empty:
        print("Não foi possível baixar os dados")
        return

    # Conversão de Fuso e Filtros
    dados_gerais.index = dados_gerais.index.tz_convert('America/Sao_Paulo')
    
    # Filtro para pegar das 10h até as 16h
    mask_horario = (
        (dados_gerais.index.hour >= 10) & 
        (
            (dados_gerais.index.hour < 16) | 
            ((dados_gerais.index.hour == 16) & (dados_gerais.index.minute == 0))
        )
    )
    dados_gerais = dados_gerais[mask_horario]

    # Dados de Interpolação (Todas as Horas Cheias disponíveis)
    dados_interpolacao = dados_gerais[dados_gerais.index.minute == 0]

    x_treino = dados_interpolacao.index.hour.tolist()
    y_treino = dados_interpolacao['Close'].values.flatten().tolist()

    print(f"\nPontos de Interpolação:")
    for h, p in zip(x_treino, y_treino):
        print(f"{h}h - R$ {p:.2f}")

    # Interação com o Usuário
    try:
        x_alvo = float(input("\nDigite o horário alvo: "))
        if not (10 <= x_alvo <= 16):
            print("O horário deve estar entre 10 e 16")
            return
    except ValueError:
        print("Valor inválido.")
        return
        
    print("\n1 - Newton")
    print("2 - Quadrática")
    print("3 - Ambos os métodos")
    opcao_metodo = input("Escolha o método de interpolação: ")

    # Variáveis comuns
    hora_exibicao = int(x_alvo)
    minuto_exibicao = int((x_alvo - hora_exibicao) * 60)
    
    # Prepara dados para o gráfico (Reais)
    x_gerais_plot = dados_gerais.index.hour + dados_gerais.index.minute / 60.0
    y_gerais_plot = dados_gerais['Close'].values.flatten()

    if opcao_metodo in ['1', '2']:
        resultado = 0.0
        metodo_nome = ""
        x_usados_calc = [] 
        y_usados_calc = []
        func_plot = None

        if opcao_metodo == '1':
            metodo_nome = "Newton"
            x_usados_calc = x_treino
            y_usados_calc = y_treino
            resultado = interpoladorDiferencasDivididas(x_treino, y_treino, x_alvo)
            func_plot = lambda x: interpoladorDiferencasDivididas(x_treino, y_treino, x)

        elif opcao_metodo == '2':
            metodo_nome = "Quadrática"
            horas_fixas = [10, 13, 16]
            x_usados_calc = []
            y_usados_calc = []
            
            for h_fixa in horas_fixas:
                idx = x_treino.index(h_fixa)
                x_usados_calc.append(x_treino[idx])
                y_usados_calc.append(y_treino[idx])
            
            resultado = interpolacaoQuadratica(x_usados_calc, y_usados_calc, x_alvo)            
            func_plot = lambda x: interpolacaoQuadratica(x_usados_calc, y_usados_calc, x)

        # Exibição Resultado (1 e 2)
        print("\nResultado da Interpolação pelo método", metodo_nome)
        print(f"O valor interpolado às {hora_exibicao}:{minuto_exibicao:02d}h foi R$ {resultado:.4f}")

        x_curva = np.linspace(10, 16, 200)
        y_curva = [func_plot(val) for val in x_curva]

        plt.figure(figsize=(12, 7))
        plt.plot(x_gerais_plot, y_gerais_plot, color='black', linewidth=1.5, label='Dados Reais', zorder=2)
        plt.plot(x_curva, y_curva, color='red', linewidth=2, label=f'Polinômio {metodo_nome}', zorder=3)
        plt.scatter(x_treino, y_treino, color='red', s=50, label='Horas Cheias', zorder=4)

        if opcao_metodo == '2':
            plt.scatter(x_usados_calc, y_usados_calc, color='red', s=120, marker='o', facecolors='none', linewidth=2, label='Pontos Fixos', zorder=5)
        
        plt.scatter([x_alvo], [resultado], color='blue', marker='*', s=250, label=f'Alvo', zorder=6)

        plt.title(f"Interpolação {metodo_nome} - {ticker} (19/11/2025)", fontsize=14)
        plt.xlabel("Hora do Dia")
        plt.ylabel("Preço (R$)")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xticks(range(10, 17)) 
        
        nome_arquivo = f"grafico_{ticker}_{metodo_nome}.png"
        plt.savefig(nome_arquivo, dpi=300)
        print(f"\nO gráfico foi salvo como '{nome_arquivo}' na pasta do projeto")

    elif opcao_metodo == '3':       
        # 1. Dados para Quadrática
        horas_fixas = [10, 13, 16]
        x_quad = []
        y_quad = []
        for h in horas_fixas:
                idx = x_treino.index(h)
                x_quad.append(x_treino[idx])
                y_quad.append(y_treino[idx])

        # 2. Cálculos
        res_newton = interpoladorDiferencasDivididas(x_treino, y_treino, x_alvo)
        res_quad = interpolacaoQuadratica(x_quad, y_quad, x_alvo)

        print(f"\nEstimativa para {hora_exibicao}:{minuto_exibicao:02d}h:")
        print(f"Newton: R$ {res_newton:.4f}")
        print(f"Quadrática: R$ {res_quad:.4f}")

        # 3. Preparando curvas
        x_curva = np.linspace(10, 16, 200)
        y_curve_newton = [interpoladorDiferencasDivididas(x_treino, y_treino, val) for val in x_curva]
        y_curve_quad = [interpolacaoQuadratica(x_quad, y_quad, val) for val in x_curva]

        # 4. Plotagem Comparativa (Preto, Azul, Vermelho)
        plt.figure(figsize=(12, 7))

        # Real (Preto)
        plt.plot(x_gerais_plot, y_gerais_plot, color='black', linewidth=1.5, label='Dados Reais (5min)', zorder=1)
        
        # Newton (Azul)
        plt.plot(x_curva, y_curve_newton, color='blue', linewidth=2, linestyle='-', label='Newton', zorder=2)
        
        # Quadrática (Vermelho)
        plt.plot(x_curva, y_curve_quad, color='red', linewidth=2, linestyle='-', label='Quadrática', zorder=3)

        # Pontos
        plt.scatter(x_treino, y_treino, color='blue', s=40, label='Pontos Newton', zorder=4)
        plt.scatter(x_quad, y_quad, color='red', s=100, marker='o', label='Pontos Quadrática', zorder=5)

        # Alvos
        plt.scatter([x_alvo], [res_newton], color='blue', marker='*', s=150, zorder=6)
        plt.scatter([x_alvo], [res_quad], color='red', marker='*', s=150, zorder=6)

        plt.title(f"Comparativo: Newton vs Quadrática - {ticker}", fontsize=14)
        plt.xlabel("Hora do Dia")
        plt.ylabel("Preço (R$)")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xticks(range(10, 17))
        
        nome_arquivo = f"grafico_{ticker}_comparativo.png"
        plt.savefig(nome_arquivo, dpi=300)
        print(f"\nO gráfico comparativo foi salvo como '{nome_arquivo}' na pasta do projeto")

    else:
        print("Opção inválida")

if __name__ == "__main__":
    main()