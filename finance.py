import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.title('Interactive Stock Dashboard Web App')

st.markdown(
    """
    Halo! Di Stock Dashboard ini berfungsi untuk mengetahui dan memantau dari beberapa saham, lho!
    Ditampilkan dalam bentuk line chart! Soo, it will be interesting to yall guys! 
    Happy to try and fill!
"""
)

tickers = ('TSLA', 'AAPL', 'MSFT', 'BTC-USD', 'ETH-USD')

dropdown = st.multiselect('Pick your assets',
                            tickers)
start = st.date_input('Start', value = pd.to_datetime('2021-01-01'))
end = st.date_input('End',value = pd.to_datetime('today'))

def relativeret(df):
    rel = df.pct_change()
    cumret = (1+rel).cumprod() - 1
    cumret = cumret.fillna(0)
    return cumret

if len(dropdown) > 0:
    #df = yf.download(dropdown,start,end)['Adj Close']
    df = relativeret(yf.download(dropdown, start, end)['Adj Close'])
    st.header('Returns of {}'.format(dropdown))
    st.line_chart(df)

st.title("Interactive Restaurant Dashboard Web App")

dataset = pd.read_excel('sales.xlsx')

st.sidebar.header("Filter By:")

category = st.sidebar.multiselect("Filter By Category:",
                                 options=dataset["CATEGORY"].unique(),
                                 default=dataset["CATEGORY"].unique())
selection_query= dataset.query(
    "CATEGORY== @category"  
)

total_profit = (selection_query["PROFIT"].sum())
avg_rating = round((selection_query["AVG_RATING"].mean()),2)

first_column, second_column = st.columns(2)

with first_column:
    st.markdown("### Total Profit:")
    st.subheader(f'{total_profit} $')
with second_column:
    st.markdown("### AVG Products Rating")
    st.subheader(f'{avg_rating}')

st.markdown("---")

profit_by_category = (selection_query.groupby(by=["CATEGORY"]).sum()[["PROFIT"]])

profit_by_category_barchart = px.bar(profit_by_category,
                              x = "PROFIT",
                              y = profit_by_category.index,
                              title = "Profit By Category",
                              color_discrete_sequence=["#17f50c"],
                              )
profit_by_category_barchart.update_layout(plot_bgcolor = "rgba(0,0,0,0)", xaxis = (dict(showgrid= False)))

profit_by_category_piechart = px.pie(profit_by_category, names = profit_by_category.index, values= "PROFIT", title = "Profit % By Category", hole=.3, color= profit_by_category.index, color_discrete_sequence=px.colors.sequential.RdPu_r)

left_column, right_column = st.columns(2)
left_column.plotly_chart(profit_by_category_barchart, use_container_width=True)
right_column.plotly_chart(profit_by_category_piechart, use_container_width=True)

hide= """
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden}
    </style>
"""
st.markdown(hide, unsafe_allow_html=True)