import yfinance as yf
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Importando os módulos da pasta Métodos
from Métodos.diferencasDivididas import interpoladorDiferencasDivididas
# Certifique-se de que o arquivo quadratica_sistemas.py existe na pasta Métodos
from Métodos.quadratica import interpolacaoQuadratica

def main():
    print("--- Sistema de Interpolação de Preços (Intraday) ---")
    print("Data Fixa: 19/11/2025\n")

    # --- Menu de Escolha de Ações ---
    acoes = {
        '1': 'PETR4.SA', '2': 'VALE3.SA', '3': 'ITUB4.SA', 
        '4': 'BBDC4.SA', '5': 'BBAS3.SA'
    }

    print("Escolha uma ação para análise:")
    for k, v in acoes.items():
        print(f"{k} - {v}")
    
    escolha_acao = input("Opção: ")
    ticker = acoes.get(escolha_acao)

    if not ticker:
        print("Opção inválida. Encerrando.")
        return

    # 1. Obtenção da Fonte Geral
    print(f"\nBaixando dados de {ticker} com intervalo de 5 minutos...")
    dados_gerais = yf.download(ticker, start="2025-11-19", end="2025-11-20", interval="5m", progress=False)

    if dados_gerais.empty:
        print("Erro: Não foi possível baixar os dados.")
        return

    # Conversão de Fuso e Filtros
    dados_gerais.index = dados_gerais.index.tz_convert('America/Sao_Paulo')
    
    # Filtro para pegar das 10h até as 16h (inclusive)
    mask_horario = (
        (dados_gerais.index.hour >= 10) & 
        (
            (dados_gerais.index.hour < 16) | 
            ((dados_gerais.index.hour == 16) & (dados_gerais.index.minute == 0))
        )
    )
    dados_gerais = dados_gerais[mask_horario]

    # 2. Dados de Interpolação (Todas as Horas Cheias disponíveis)
    dados_interpolacao = dados_gerais[dados_gerais.index.minute == 0]

    x_treino = dados_interpolacao.index.hour.tolist()
    y_treino = dados_interpolacao['Close'].values.flatten().tolist()

    print(f"\nPontos de Interpolação coletados (Horas Cheias):")
    for h, p in zip(x_treino, y_treino):
        print(f"Hora: {h}h -> Preço: R$ {p:.2f}")

    # 3. Interação com o Usuário
    print("\n--- Entrada de Dados ---")
    try:
        x_alvo_str = input("Digite o horário alvo (ex: 12.5 para 12h30min) [entre 10 e 16]: ")
        x_alvo = float(x_alvo_str)
        
        if not (10 <= x_alvo <= 16):
            print("Erro: O horário deve estar entre 10 e 16.")
            return
            
        print("\nEscolha o método de interpolação:")
        print("1 - Newton (Diferenças Divididas - Usa todos os pontos)")
        print("2 - Quadrática (Sistema Linear - Usa FIXOS: 10h, 13h, 16h)")
        opcao_metodo = input("Opção: ")

        resultado = 0.0
        metodo_nome = ""
        
        # Variáveis para armazenar contexto do plot
        x_usados_calc = [] 
        y_usados_calc = []
        func_plot = None

        if opcao_metodo == '1':
            metodo_nome = "Newton"
            # Newton usa TODOS os pontos disponíveis
            x_usados_calc = x_treino
            y_usados_calc = y_treino
            resultado = interpoladorDiferencasDivididas(x_treino, y_treino, x_alvo)
            
            func_plot = lambda x: interpoladorDiferencasDivididas(x_treino, y_treino, x)

        elif opcao_metodo == '2':
            metodo_nome = "Quadrática (10h, 13h, 16h)"
            
            # --- LÓGICA ALTERADA AQUI ---
            # Seleciona apenas os dados correspondentes a 10, 13 e 16
            horas_fixas = [10, 13, 16]
            
            # Filtra as listas x_treino e y_treino baseada nas horas fixas
            x_usados_calc = []
            y_usados_calc = []
            
            for h_fixa in horas_fixas:
                try:
                    # Encontra o índice onde a hora é igual a h_fixa
                    idx = x_treino.index(h_fixa)
                    x_usados_calc.append(x_treino[idx])
                    y_usados_calc.append(y_treino[idx])
                except ValueError:
                    print(f"Aviso: Dados para a hora {h_fixa}h não encontrados.")
            
            if len(x_usados_calc) != 3:
                print("Erro: Não foram encontrados os 3 pontos fixos (10, 13, 16) na base de dados.")
                return

            print(f"Pontos selecionados para o sistema: {x_usados_calc}")
            
            resultado = interpolacaoQuadratica(x_usados_calc, y_usados_calc, x_alvo)
            
            # Função lambda usa apenas os 3 pontos fixos para desenhar a parábola
            func_plot = lambda x: interpolacaoQuadratica(x_usados_calc, y_usados_calc, x)
            
        else:
            print("Opção inválida.")
            return

        # 5. Exibição do Resultado
        hora_exibicao = int(x_alvo)
        minuto_exibicao = int((x_alvo - hora_exibicao) * 60)
        
        print("-" * 30)
        print(f"Preço Estimado ({metodo_nome}) às {hora_exibicao}:{minuto_exibicao:02d}h: R$ {resultado:.4f}")
        print("-" * 30)

        # 6. PLOTAGEM DOS GRÁFICOS
        print("\nGerando gráfico...")

        # A) Dados Reais
        x_gerais_plot = dados_gerais.index.hour + dados_gerais.index.minute / 60.0
        y_gerais_plot = dados_gerais['Close'].values.flatten()

        # B) Curva Interpolada
        x_curva = np.linspace(10, 16, 200)
        y_curva = [func_plot(val) for val in x_curva]

        plt.figure(figsize=(12, 7))
        
        # 1. Linha Preta: Dados Reais
        plt.plot(x_gerais_plot, y_gerais_plot, color='black', linewidth=1.5, label='Dados Reais (5 min)', zorder=2)
        
        # 2. Linha Azul: Polinômio Interpolador
        plt.plot(x_curva, y_curva, color='blue', linewidth=2, label=f'Polinômio ({metodo_nome})', zorder=3)
        
        # 3. Pontos Vermelhos: Todas as horas cheias disponíveis (para mostrar o contexto)
        plt.scatter(x_treino, y_treino, color='red', s=50, label='Horas Cheias (Disponíveis)', zorder=4)

        # 4. Destaque Laranja: Pontos efetivamente usados no cálculo
        if opcao_metodo == '2':
             plt.scatter(x_usados_calc, y_usados_calc, color='orange', s=120, marker='o', facecolors='none', edgecolors='orange', linewidth=2, label='Pontos Fixos (10h, 13h, 16h)', zorder=5)
        
        # 5. Estrela Verde: O alvo
        plt.scatter([x_alvo], [resultado], color='green', marker='*', s=250, label=f'Alvo ({hora_exibicao}:{minuto_exibicao:02d})', zorder=6)

        plt.title(f"Interpolação {metodo_nome} - {ticker} (19/11/2025)", fontsize=14)
        plt.xlabel("Hora do Dia")
        plt.ylabel("Preço (R$)")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xticks(range(10, 17)) 
        
        plt.show()

    except ValueError:
        print("Erro: Digite um número válido.")

if __name__ == "__main__":
    main()