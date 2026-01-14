import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objs as go
from streamlit_autorefresh import st_autorefresh

# Lista de países e intervalos disponíveis para seleção
countries = ["Brazil", "United States"]
intervals = [
    "1d",
    "1wk",
    "1mo",
]  # Intervalos suportados pelo yfinance: 1 dia, 1 semana, 1 mês

start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()


# Buscar dados de ações com cache para evitar requisições redundantes à API
@st.cache_data()
def fetch_stock_data(stock, from_date, to_date, interval):
    """
    Recupera dados históricos de ações do Yahoo Finance.

    Args:
        stock (str): Símbolo do ticker da ação (ex: 'AAPL')
        from_date (str): Data inicial no formato 'YYYY-MM-DD'
        to_date (str): Data final no formato 'YYYY-MM-DD'
        interval (str): Intervalo de dados ('1d', '1wk', '1mo')

    Returns:
        DataFrame: Dados históricos da ação com valores OHLC (Abertura, Máxima, Mínima, Fechamento)
    """
    return yf.download(
        stock, start=from_date, end=to_date, interval=interval, progress=False
    )


# Formata objeto datetime para representação em string
def format_date(dt, format="%Y-%m-%d"):
    """
    Converte objeto datetime para formato string.

    Args:
        dt (datetime): Objeto datetime a formatar
        format (str): Cadeia de formato de data (padrão: 'YYYY-MM-DD')

    Returns:
        str: String de data formatada
    """
    return dt.strftime(format)


# Gera gráfico de candlestick a partir de dados OHLC
def plot_candlestick(df, ticker="UNKNOWN"):
    """
    Cria um gráfico de candlestick interativo a partir de dados OHLC.

    Args:
        df (DataFrame): Dados da ação com colunas OHLC
        ticker (str): Símbolo do ticker da ação para legenda do gráfico

    Returns:
        Figure: Figura de gráfico de candlestick do Plotly
    """
    trace1 = {
        "x": df.index,
        "open": df["Open"],
        "close": df["Close"],
        "high": df["High"],
        "low": df["Low"],
        "type": "candlestick",
        "name": ticker,
        "showlegend": False,
    }

    data = [trace1]
    layout = go.Layout()

    return go.Figure(data=data, layout=layout)


# Construir barra lateral com controles de entrada do usuário
sidebar_placeholder = st.sidebar.empty()
country_select = st.sidebar.selectbox("Selecione o país:", countries)
stocks = [
    "AAPL",
    "MSFT",
    "GOOGL",
]  # Lista de ações - customize com os tickers desejados
stock_select = st.sidebar.selectbox("Selecione a ação:", stocks)
from_date = st.sidebar.date_input("Data Inicial:", start_date)
to_date = st.sidebar.date_input("Data Final:", end_date)
interval_select = st.sidebar.selectbox("Selecione o intervalo:", intervals)
load_data = st.sidebar.checkbox("Carregar Dados")

# Contêineres placeholder para renderização dinâmica de gráficos
chart_line = st.empty()
chart_candlestick = st.empty()

# Cabeçalho e título da página
st.title("Análise Gráfica de Ações em Tempo Real")
st.header("Ações")
st.subheader("Análise Gráfica")

# Atualizar página a cada 5 segundos (máximo 10000 atualizações)
count = st_autorefresh(interval=5000, limit=10000, key="fizzbuzzcounter")

if count == 0:
    st.write("Contagem é zero")
elif count % 3 == 0 and count % 5 == 0:
    st.write("FizzBuzz")
elif count % 3 == 0:
    st.write("Fizz")
elif count % 5 == 0:
    st.write("Buzz")
else:
    st.write(f"Contagem: {count}")

# Validar intervalo de datas e buscar/exibir dados de ações
if from_date > to_date:
    st.sidebar.error("Data Inicial não pode ser maior que Data Final")
else:
    df = fetch_stock_data(
        stock_select, format_date(from_date), format_date(to_date), interval_select
    )
    try:
        # Exibir gráfico de candlestick
        fig = plot_candlestick(df, stock_select)
        chart_candlestick.plotly_chart(fig)

        # Exibir gráfico de linha do preço de fechamento
        chart_line.line_chart(df["Close"])

        # Opcionalmente exibir tabela de dados brutos
        if load_data:
            st.subheader("Dados")
            st.dataframe(df)
    except Exception as e:
        st.error(f"Erro ao carregar dados da ação: {e}")
