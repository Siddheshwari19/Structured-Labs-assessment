from preswald import text, plotly, connect, get_df, table, slider
import pandas as pd
import plotly.express as px
from preswald import query

# Display a welcoming message with a heading
text("# ☕ Brew It and View It: Coffee Trends Unfiltered")

# Load the CSV data
connect()
df = get_df('coffee_data')

# Clean and prepare the data
df['datetime'] = pd.to_datetime(df['datetime'])
df['hour'] = df['datetime'].dt.hour
df['date'] = pd.to_datetime(df['date'])

# SQL Query for a quick peek at the data
sql = "SELECT * FROM coffee_data LIMIT 5"
filtered_df = query(sql, "coffee_data")

# Key Performance Indicators (KPIs)
total_sales = df['money'].sum()
total_transactions = df.shape[0]
unique_coffees = df['coffee_name'].nunique()

# 1. **Top Selling Coffee Drinks** (Bar Chart)
top_coffees = df['coffee_name'].value_counts().reset_index()
top_coffees.columns = ['coffee_name', 'count']
fig_top = px.bar(top_coffees, x='coffee_name', y='count', 
                 title=" Top Selling Coffee Drinks",
                 labels={'count': 'Number of Transactions', 'coffee_name': 'Coffee'},
                 color='count', color_continuous_scale='YlOrBr')

fig_top.update_layout(
    template='plotly_white',
    xaxis_title="Coffee Type",
    yaxis_title="Number of Transactions",
    title_font=dict(size=20)
)

# Description for the "Top Selling Coffee Drinks" chart
text("""
### Top Selling Coffee Drinks
This bar chart displays the most popular coffee drinks based on the number of transactions. 
It allows us to quickly identify which coffee drinks are in high demand. 
The color scale reflects the volume of sales, with darker colors representing more transactions.
""")

# Display the chart
plotly(fig_top)

# 2. **Sales by Hour of Day** (Line Chart)
hourly_sales = df.groupby('hour')['money'].sum().reset_index()
fig_hour = px.line(hourly_sales, x='hour', y='money',
                   title=" Sales by Hour of Day",
                   labels={'hour': 'Hour of Day', 'money': 'Total Sales ($)'},
                   markers=True)

fig_hour.update_layout(
    template='plotly_white',
    xaxis_title="Hour of Day",
    yaxis_title="Total Sales ($)",
    title_font=dict(size=20)
)

# Description for the "Sales by Hour of Day" chart
text("""
### Sales by Hour of Day
This line chart highlights how coffee sales fluctuate throughout the day. 
It helps to visualize peak sales hours and identify potential opportunities for optimizing staffing and inventory. 
Notice the peaks during certain hours, which could indicate when customers are most likely to make a purchase.
""")

# Display the chart
plotly(fig_hour)

# 3. **Coffee Preferences by Season** (Seasonal Visualization)
def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

df['season'] = df['date'].apply(get_season)
seasonal_counts = df.groupby(['season', 'coffee_name']).size().reset_index(name='count')

fig_season = px.bar(seasonal_counts, x='coffee_name', y='count',
                    color='season', barmode='group',
                    title=' Coffee Preferences by Season',
                    labels={'coffee_name': 'Coffee Drink', 'count': 'Number of Orders'})

fig_season.update_layout(
    template='plotly_white',
    xaxis={'categoryorder':'total descending'},
    title_font=dict(size=20)
)

# Description for the "Coffee Preferences by Season" chart
text("""
### Coffee Preferences by Season
This chart compares the popularity of coffee drinks across different seasons of the year. 
It allows us to see which coffee types are favored during specific times of the year, 
helping businesses align their offerings with seasonal trends.
For instance, certain drinks might perform better in colder months (like hot coffee) compared to warmer months (such as iced coffee).
""")

# Display the chart
plotly(fig_season)

# 4. **Sales Volume by Hour and Day** (Heatmap)
df['day'] = df['datetime'].dt.day_name()
heat = df.groupby(['day', 'hour']).size().reset_index(name='count')

fig_heat = px.density_heatmap(heat, x='hour', y='day', z='count',
                              title=' Sales Volume by Hour and Day',
                              color_continuous_scale='Blues')

fig_heat.update_layout(
    template='plotly_white',
    xaxis_title="Hour of Day",
    yaxis_title="Day of Week",
    title_font=dict(size=20)
)

# Description for the "Sales Volume by Hour and Day" chart
text("""
### Sales Volume by Hour and Day
This heatmap reveals the sales volume patterns throughout the week and by hour. 
It provides valuable insights into which hours and days experience the highest transaction volumes, 
helping businesses optimize their operations, staffing, and marketing campaigns. 
The darker shades indicate higher sales, making it easy to spot trends.
""")

# Display the chart
plotly(fig_heat)

# 5. **Payment Method Distribution** (Pie Chart)
payment_counts = df['cash_type'].value_counts().reset_index()
payment_counts.columns = ['cash_type', 'count']

fig_payment = px.pie(payment_counts, names='cash_type', values='count',
                     title=' Payment Method Distribution',
                     color_discrete_sequence=px.colors.sequential.Turbo)

fig_payment.update_layout(
    template='plotly_white',
    title_font=dict(size=20)
)

# Description for the "Payment Method Distribution" chart
text("""
### Payment Method Distribution
This pie chart illustrates the distribution of payment methods used by customers. 
It provides a clear overview of how transactions are processed (e.g., cash, credit card, digital payments). 
Understanding payment method preferences can help businesses streamline their payment systems and optimize customer experience.
""")

# Display the chart
plotly(fig_payment)


# **Customer Distribution by Day of Week** - Radar Chart
weekday_counts = df['datetime'].dt.day_name().value_counts().reset_index()
weekday_counts.columns = ['day', 'count']
weekday_counts = weekday_counts.sort_values(by='day', key=lambda x: pd.to_datetime(x, format='%A'))

fig_radar = px.line_polar(weekday_counts, r='count', theta='day', line_close=True,
                          title=' Customer Visits by Day of Week',
                          color_discrete_sequence=['darkorange'])
fig_radar.update_traces(fill='toself')
fig_radar.update_layout(template='plotly_white', polar=dict(radialaxis=dict(visible=True)))

text("""
### Customer Distribution by Day of Week
This radar chart visualizes foot traffic across the week. 
It's a perfect way to spot your busiest and slowest days at a glance, helping optimize staffing and promotions.
""")

# Display the chart
plotly(fig_radar)

# 7. **Average Spend per Coffee Type** (Bar Chart)
avg_spend_coffee = df.groupby('coffee_name')['money'].mean().reset_index()

fig_avg_spend = px.bar(avg_spend_coffee, x='coffee_name', y='money',
                       title=" Average Spend per Coffee Type",
                       labels={'money': 'Average Spend ($)', 'coffee_name': 'Coffee Type'},
                       color='money', color_continuous_scale='Viridis')

fig_avg_spend.update_layout(
    template='plotly_white',
    xaxis_title="Coffee Type",
    yaxis_title="Average Spend ($)",
    title_font=dict(size=20)
)

# Description for the "Average Spend per Coffee Type" chart
text("""
### Average Spend per Coffee Type
This bar chart shows the average spend for each coffee type. 
It helps us understand the spending behavior of customers and the value of different coffee drinks. 
High average spend on certain coffee types may indicate premium offerings or popular drinks with higher prices.
""")

# Display the chart
plotly(fig_avg_spend)