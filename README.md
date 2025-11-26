# <h1 align="center" style="font-weight: bold;"> SISTEMA INTERPOLADOR DE PREÇOS</h1>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Portfolio](https://img.shields.io/badge/Portfolio-%23000000.svg?style=for-the-badge&logo=firefox&logoColor=#FF7139)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)

O Sistema Interpolador de Preços foi desenvolvido como projeto final da disciplina de Métodos Numéricos com o intuito de utilizar os métodos interpoladores de Newton (Diferenças Divididas) e Interpolação Quadrática para interpolar dados intraday da bolsa de valores. O propósito final do projeto é analisar e comparar os resultados obtidos com cada método.

# Funcionamento

O algoritmo usa o dia 19/11/2025 como data fixa, é possível escolher que ação vai ser interpolada entre as empresas Petrobras, Vale, Itau, Bradesco e Banco do Brasil. Os preços da ação escolhida são obtidos das 10h às 16h com intervalo de 1 hora através da biblioteca yfinance do python. O usuário deve informar a hora exata que deseja saber o valor da ação (por exemplo às 10.7 ou às 15.43) e em seguida informar qual método deve ser utilizado, após isso o algoritmo retorna o valor estimado da ação naquele horário e o gráfico que compara os valores reais com o valor obtido através da interpolação.

<img width="3600" height="2100" alt="image" src="https://github.com/user-attachments/assets/f209f112-33ee-4070-85a2-1672771de7ef" />
<img width="3600" height="2100" alt="image" src="https://github.com/user-attachments/assets/cdff1000-fd14-47f2-b67f-14eac84ce9c2" />

# Contextualização

O yfinance é distribuído sob a Licença de Software Apache. Não é afiliado, endossado ou verificado pela Yahoo!Inc. É uma ferramenta open-source que utiliza as APIs públicas do Yahoo! e é destinada a fins de pesquisa e educação. 
Seguem os links de termo de uso do Yahoo! para obter detalhes sobre seus direitos de uso dos dados baixados: [Yahoo Developer API Terms of Use](https://legal.yahoo.com/us/en/yahoo/terms/product-atos/apiforydn/index.html
) e [Yahoo Terms of Service](https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html
).

# Instalação

## Pré-requisitos

Além do python 3 e do pip, é necessário a instalção das bibliotecas yfinance e matplotlib.

1° passo: abrir o CMD e digitar os comandos

```pip install yfinance```

```pip install matplotlib```

## Passo a passo para execução

1° passo: clonar o repositório

```git clone https://github.com/Jhon-Victor-Ramos/projeto-metodos-numericos ```

2° passo: entrar na pasta do projeto

```cd projeto-metodos-numericos```

3° passo: executar

```python main.py```

# Contribuidores

* **Camila Torquato** - [Github](https://github.com/camilatorquato) | [LinkedIn](https://www.linkedin.com/in/camila-torquato-5b5356354/?utm_source=share_via&utm_content=profile&utm_medium=member_android)
* **Gabriella Theóphilo** - [LinkedIn](https://www.linkedin.com/in/gabriella-the%C3%B3philo-32b666348?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app) | [Instagram](https://www.instagram.com/gaab.03_?igsh=azEzMnp0cWt4dXZx) 
* **Jhon Victor Ramos Martins** - [GitHub](https://github.com/Jhon-Victor-Ramos) | [LinkedIn](https://www.linkedin.com/in/jhon-victor-ramos/) | [Instagram](https://www.instagram.com/jhonvictor_dev?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==) | [Lattes](http://lattes.cnpq.br/2282663214204464)
* **Rielly Luiza Duarte da Silva** - [GitHub](https://github.com/rluizaduarte) | [LinkedIn](https://www.linkedin.com/in/rielly-luiza-370282332?utm_source=share_via&utm_content=profile&utm_medium=member_ios) | [Instagram](https://www.instagram.com/riellylduarte?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==) | [Lattes](http://lattes.cnpq.br/0089072611329730)
