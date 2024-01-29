import streamlit as st
import pandas as pd
import numpy as np
import hvplot.pandas
import plotly.express as px
import altair as alt
import warnings
warnings.filterwarnings('ignore')

#STEAMLIT Page layout configuration
st.set_page_config(page_title="BTC vs. Vanguard Energy ETF Dashboard", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: BTC spot ETF :vs: VENAX ETF")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

# Introduction Statement
st.markdown("## Energy Sector Investment Analysis App")

st.markdown("""
Welcome to the Energy Sector Investment Analysis App! The purpose of this app is to explore the potential 
correlation between two distinct investment assets: VENAX, an Energy Sector Exchange Traded Fund (ETF), 
and Bitcoin (BTC). Both assets were selected due to their connection to the energy sector - Bitcoin 
requires significant energy for mining, and the profits of the ETF (VENAX) are tied to the energy consumption 
industry.

The chosen assets are:
- **VENAX:** An Energy Sector ETF that captures the performance of companies in the energy sector, including 
those involved in oil, gas, renewables, and related industries.
- **BTC:** The widely known cryptocurrency, Bitcoin, which relies on energy-intensive mining processes.

Our objective is to analyze and discover potential correlations or insights between these two assets, 
which share a common factor in the energy sector. By examining cumulative returns, annualized standard 
deviations, and other metrics, we aim to provide valuable insights for investors interested in the 
energy sector and its intersection with cryptocurrency investments.
""")
#BTC data
st.markdown("### BTC Dataset")
btc_df = pd.read_csv('BTC-USD_daily.csv', index_col='Date', parse_dates=True, infer_datetime_format=True)
btc_df.drop(columns=['Adj Close','High', 'Low', 'Open'], inplace=True)
btc_df.rename(columns={'Close': 'BTC close'}, inplace=True)
st.dataframe(btc_df)

# Bar chart for volume
selected_column = 'Volume'
st.markdown("### BTC Volume (in millions)")
st.bar_chart(btc_df['Volume'])


#price line chart
st.markdown("### BTC Closing Price in USD")
st.line_chart(btc_df['BTC close'])

#######################################################################################################################
#import VENAX ETF csv
st.markdown("### VENAX Dataset")
venax_df = pd.read_csv('VENAX_daily2.csv', index_col='Date', parse_dates=True, infer_datetime_format=True)
venax_df.head()

#rename close column
venax_df.rename(columns={'Close': 'VENAX close'}, inplace=True)
venax_df

#venax line chart of price
st.markdown("### VENAX Closing Price")
st.line_chart(venax_df['VENAX close'])

###########################################################################################################################
#transition to analysis
st.header(' :chart_with_upwards_trend: Analysis :chart_with_downwards_trend: ')

#combined dataframes
combined_df = pd.concat([venax_df, btc_df], axis=1, join='outer').pct_change()

#dropnas
combined_df.dropna(subset=['VENAX close','BTC close'])

#daily retuns chart
st.markdown("#### Daily Returns Chart")


#plotting

# Slider to select the time range if wanted
start_date = st.date_input('Start Date', pd.to_datetime('2017-01-20'))
end_date = st.date_input('End Date', pd.to_datetime('2024-01-17'))


# Create the Plotly figure
fig1 = px.line(combined_df, x=combined_df.index, y=['VENAX close', 'BTC close'], title='Daily returns')
fig1.update_xaxes(title_text='Date')
fig1.update_yaxes(title_text='Close Price')

# Adjust the width of the chart
fig1.update_layout(width=1700)

#Display the interactive chart
st.plotly_chart(fig1)

#scatter plot visualizer
st.markdown("### Scatter Plot Chart")

# Create the Plotly Express scatter plot
fig2 = px.scatter(combined_df, x=combined_df.index, y=['VENAX close', 'BTC close'], title='Scatter plot Chart', 
                  labels={'y': 'Close Price'}, range_x=['2017-01-01', '2024-01-01'])
fig2.update_xaxes(title_text='Date')

# Adjust the width of the chart
fig2.update_layout(width=1500)
# Display the scatter plot
st.plotly_chart(fig2)

# box plot
st.markdown("### Risk Assesment")

# Melt the df to create a long format for Altair?
melted_df = combined_df.melt(value_vars=['VENAX close', 'BTC close'], var_name='Asset', value_name='Close')

# Create a box plot using Altair
box_plot = alt.Chart(melted_df).mark_boxplot().encode(
    x='Asset:N',
    y='Close:Q'
).properties(
    width=800,
    height=800
)

# Display the Altair chart using st.altair_chart()
st.altair_chart(box_plot)

st.markdown("### Cumulative Returns Plot")

# Calculate cumulative returns
cumulative_df = (1 + combined_df).cumprod()

# Plot cumulative returns using st.line_chart()
st.line_chart(cumulative_df)

##cumulative returns std
cum_returns_std = cumulative_df.std()

annulized_std = cum_returns_std * np.sqrt(252)


st.markdown("### Correlation Heatmap")

# Calculate the correlation
correlation_matrix = cumulative_df.corr()

# Create a heatmap with Plotly Express
fig = px.imshow(correlation_matrix, labels=dict(x="Asset", y="Asset", color="Correlation"),
                x=correlation_matrix.index, y=correlation_matrix.columns,
                color_continuous_scale="Viridis")

# Display the heatmap using st.plotly_chart()
st.plotly_chart(fig)

# Create two columns
col1, col2 = st.columns(2)

# Display metrics in separate columns
with col1:
    st.metric(label="Cumulative Returns - VENAX", value=0.218971)
    st.metric(label="Annualized Std Dev - VENAX", value=3.476051)

with col2:
    st.metric(label="Cumulative Returns - BTC", value=18.109523)
    st.metric(label="Annualized Std Dev - BTC", value=287.479770)


# Financial Analysis Summary
st.markdown("## Financial Analysis Summary")

st.markdown("""
In the conducted financial analysis, we assessed the performance of two investments: Vanguard Energy ETF "VENAX" and Bitcoin. 
The cumulative returns over the analyzed period reveal that BTC has significantly outperformed VENAX, 
with cumulative returns of 18.11 compared to VENAX's 0.22. This indicates that BTC has been more profitable 
over the given timeframe.

However, when it comes to risk, the annualized standard deviation presents a different perspective. 
VENAX exhibits a lower annualized standard deviation of 3.48, suggesting lower volatility and less risk 
compared to BTC, which has an annualized standard deviation of 287.48. In terms of risk mitigation, VENAX 
emerges as the better hedge against risk.

In conclusion, while BTC has shown higher profitability, it comes with greater volatility and risk. 
On the other hand, VENAX, with its lower risk profile, may be considered a safer investment, albeit with 
lower returns.
""")




