import yfinance as yf
import plotly.graph_objs as go
import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots

# Set up the Streamlit app
st.title("Stock Chart Viewer")

# Input for the stock ticker symbol
ticker = st.text_input("Enter the stock ticker symbol", "AAPL")
start_date = st.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("2024-01-01"))

# Button to fetch and plot the data
if st.button("Fetch and Plot"):
    data = yf.download(ticker, start=start_date, end=end_date)

    # Calculate moving averages
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()

    # Create Candlestick Chart with Moving Averages
    candlestick_chart = make_subplots(rows=1, cols=1)

    candlestick_chart.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Candlestick',
        increasing_line_color='green',
        decreasing_line_color='red'
    ))

    candlestick_chart.add_trace(go.Scatter(
        x=data.index,
        y=data['MA20'],
        mode='lines',
        name='MA20',
        line=dict(color='blue', width=1)
    ))

    candlestick_chart.add_trace(go.Scatter(
        x=data.index,
        y=data['MA50'],
        mode='lines',
        name='MA50',
        line=dict(color='orange', width=1)
    ))

    candlestick_chart.update_layout(
        title=f'{ticker} Candlestick Chart with Moving Averages',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='LightGrey'),
        yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='LightGrey'),
        template='plotly_dark',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )

    candlestick_chart.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    # Display the chart in Streamlit
    st.plotly_chart(candlestick_chart)
