import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objs as go

# List of countries and intervals available for selection
countries = ["Brazil", "United States"]
intervals = [
    "1d",
    "1wk",
    "1mo",
]  # Supported intervals by yfinance: 1 day, 1 week, 1 month

start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()


# Fetch stock data with cache to avoid redundant API requests
@st.cache_data()
def fetch_stock_data(stock, from_date, to_date, interval):
    """
    Retrieve historical stock data from Yahoo Finance.

    Args:
        stock (str): Ticker symbol (e.g. 'AAPL')
        from_date (str): Start date in 'YYYY-MM-DD' format
        to_date (str): End date in 'YYYY-MM-DD' format
        interval (str): Data interval ('1d', '1wk', '1mo')

    Returns:
        DataFrame: Historical OHLC stock data (Open, High, Low, Close)
    """
    return yf.download(
        stock, start=from_date, end=to_date, interval=interval, progress=False
    )


# Format a datetime object to a string representation
def format_date(dt, format="%Y-%m-%d"):
    """
    Convert a datetime object to a formatted string.

    Args:
        dt (datetime): Datetime object to format
        format (str): Date format string (default: 'YYYY-MM-DD')

    Returns:
        str: Formatted date string
    """
    return dt.strftime(format)


# Generate a candlestick chart from OHLC data
def plot_candlestick(df, ticker="UNKNOWN"):
    """
    Create an interactive candlestick chart from OHLC data.

    Args:
        df (DataFrame): Stock data with OHLC columns
        ticker (str): Ticker symbol for the chart legend

    Returns:
        Figure: Plotly candlestick figure
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


# Build sidebar with user input controls
sidebar_placeholder = st.sidebar.empty()
country_select = st.sidebar.selectbox("Select Country:", countries)
stocks = [
    "AAPL",
    "MSFT",
    "GOOGL",
]  # List of stocks - customize with desired tickers
stock_select = st.sidebar.selectbox("Select Stock:", stocks)
from_date = st.sidebar.date_input("Start Date:", start_date)
to_date = st.sidebar.date_input("End Date:", end_date)
interval_select = st.sidebar.selectbox("Select Interval:", intervals)
load_data = st.sidebar.checkbox("Show Raw Data")


# Placeholder containers for dynamic chart rendering
chart_line = st.empty()
chart_candlestick = st.empty()

# Page header and title
st.title("Real-time Stock Chart Analysis")
st.header("Stock Overview")
st.subheader("Interactive Analysis")

if st.sidebar.button("Refresh Data"):
    st.experimental_rerun()

# Validate date range and fetch/display stock data
if from_date > to_date:
    st.sidebar.error("Start Date cannot be later than End Date")
else:
    df = fetch_stock_data(
        stock_select, format_date(from_date), format_date(to_date), interval_select
    )
    try:
        # Display candlestick chart
        fig = plot_candlestick(df, stock_select)
        chart_candlestick.plotly_chart(fig)

        # Display closing price line chart
        chart_line.line_chart(df["Close"])

        # Optionally display raw data table
        if load_data:
            st.subheader("Data")
            st.dataframe(df)
    except Exception as e:
        st.error(f"Error loading stock data: {e}")
