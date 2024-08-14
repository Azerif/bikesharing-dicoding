import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# create function for each data visualization


def create_daily_rent(df):
    daily_rent_df = df.resample(rule='D', on='dteday').agg({
        'cnt': 'sum',
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()

    return daily_rent_df


def create_count_weathers(df):
    count_weathers_df = df.groupby(by='weathersit').agg({
        'cnt': 'sum',
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()

    # Reshape the DataFrame to make plotting easier
    weathers_melted_df = count_weathers_df.melt(
        id_vars='weathersit',
        value_vars=['cnt', 'casual', 'registered'],
        var_name='Type',
        value_name='Count'
    )

    return weathers_melted_df


def create_count_season_weathers(df):
    season_weather_df = df.groupby(by=['season', 'weathersit']).agg({
        'cnt': 'sum',
    }).reset_index()

    return season_weather_df


def create_count_weekend(df):
    count_weekend_df = df.groupby(by='weekend').agg({
        'cnt': 'mean'
    }).reset_index()

    # Changing column 'weekend' with more descriptive label
    count_weekend_df['weekend'] = count_weekend_df['weekend'].map({
        0: 'Workday',
        1: 'Weekend'
    })

    return count_weekend_df


def create_rfm(df):
    rfm_df = day_df.groupby(by='weathersit', as_index=False).agg({
        'dteday': 'max',      # taking last order data
        'instant': 'nunique',  # taking order count
        # because there was no revenue, therefore we use cnt (count rentals)
        'cnt': 'sum'
    })

    rfm_df.columns = ['weathers',
                      'max_order_timestamp', 'frequency', 'monetary']

    rfm_df['max_order_timestamp'] = rfm_df['max_order_timestamp'].dt.date
    recent_date = day_df['dteday'].dt.date.max()
    rfm_df['recency'] = rfm_df['max_order_timestamp'].apply(
        lambda x: (recent_date - x).days)

    rfm_df.drop('max_order_timestamp', axis=1, inplace=True)
    return rfm_df


# load csv
data_path = 'dashboard/cleaned_day.csv'
day_df = pd.read_csv(data_path)

# create a time range so that data visualization can be displayed based on a specific date range
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)

day_df['dteday'] = pd.to_datetime(day_df['dteday'])

min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

with st.sidebar:
    # adding logo
    st.image("dashboard/bikesharing.png")

    start_date, end_date = st.date_input(
        label='Date Filter', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

day_df = day_df[(day_df["dteday"] >= str(start_date)) &
                (day_df["dteday"] <= str(end_date))]

# using each function
daily_rent_df = create_daily_rent(day_df)
count_weathers_df = create_count_weathers(day_df)
season_weathers_df = create_count_season_weathers(day_df)
count_weekend_df = create_count_weekend(day_df)
rfm_df = create_rfm(day_df)

st.header('Bike Sharing Dataset :bike:')
with st.expander('Data Preview'):
    st.dataframe(
        day_df,
        column_config={  # change coma with decimal format
            'yr': st.column_config.NumberColumn(format='%d'),
            'cnt': st.column_config.NumberColumn(format='%d'),
            'casual': st.column_config.NumberColumn(format='%d'),
            'registered': st.column_config.NumberColumn(format='%d')
        }

    )

# display daily bike sharing

st.subheader('Daily Bike Sharing Count based on Date')
col1, col2, col3 = st.columns(3)

with col1:
    total_orders = daily_rent_df['cnt'].sum()
    st.metric("Total Bike Sharing Count", value=total_orders)

with col2:
    total_sum = daily_rent_df['casual'].sum()
    st.metric("Total Casual", value=total_sum)

with col3:
    total_sum = daily_rent_df['registered'].sum()
    st.metric("Total Registered", value=total_sum)

colors_ = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green

# display User Type on Weather Conditions barplot
st.subheader('User Type on Weather Conditions')

count_weathers_df = count_weathers_df.sort_values(by='Count', ascending=False)

fig = plt.figure(figsize=(10, 6))

sns.barplot(x='weathersit', y='Count', hue='Type',
            palette=colors_, data=count_weathers_df)
plt.title('Total User Type Count by Weather Condition')
plt.xlabel(None)
plt.ylabel(None)
plt.legend(title='User Type')

for container in plt.gca().containers:
    plt.bar_label(container, fmt='%.0f', label_type='edge',
                  fontsize=10, padding=2)

st.pyplot(fig)


# display Weather Conditions in Different Season
st.subheader('Weather Conditions in Different Seasons')

fig = plt.figure(figsize=(10, 6))
sns.barplot(x='season', y='cnt', hue='weathersit', data=season_weathers_df.sort_values(by='cnt', ascending=False),
            palette=colors_, dodge=True)

plt.title('Total Count by Season and Weather Situation', fontsize=20)
plt.xlabel(None)
plt.ylabel(None)
plt.legend(title='Weather Situation', title_fontsize='13', fontsize='12')

for container in plt.gca().containers:
    plt.bar_label(container, fmt='%.0f', label_type='edge',
                  fontsize=10, padding=2)
plt.tight_layout()
st.pyplot(fig)


# display Temperature Scatter Plot and Average Rental Bike Bar Plot

st.subheader('Temperature Impact')
fig = plt.figure(figsize=(12, 8))
sns.scatterplot(data=day_df, x='temp', y='cnt', color='blue',
                label='Temperature', alpha=0.5, marker='o')

sns.scatterplot(data=day_df, x='atemp', y='cnt', color='green',
                label='Feels-like Temperature', alpha=0.5, marker='o')

# Menambahkan garis linear untuk temp
sns.regplot(data=day_df, x='temp', y='cnt', scatter=False, color='blue')
# Menambahkan garis linear untuk atemp
sns.regplot(data=day_df, x='atemp', y='cnt', scatter=False, color='green')

plt.title('Effect of Temperature on the Number of Bike Sharing Usage')
plt.xlabel(None)
plt.ylabel(None)
plt.legend()
st.pyplot(fig)


st.subheader('Average Bike Sharing Usage')
fig = plt.figure(figsize=(10, 3))
sns.barplot(x='weekend', y='cnt', hue='weekend',
            data=count_weekend_df, palette='viridis')
plt.title('Average Bike Sharing Usage based on Day Types')
plt.xlabel(None)
plt.ylabel(None)
plt.tight_layout()
st.pyplot(fig)


st.subheader('RFM Analysis of Bike Sharing Usage Based on Weather Conditions')
col1, col2 = st.columns(2)

colors = ["#72BCD4", "#72BCD4", "#72BCD4"]
with col1:
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(
        y='recency', x='weathers',
        data=rfm_df.sort_values(by='recency', ascending=True),
        palette=colors, hue='weathers', legend=False
    )
    plt.ylabel(None)
    plt.xlabel(None)
    plt.title('By Recency (weathers)', loc='center', fontsize=18)
    plt.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)

with col2:
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(
        y='frequency', x='weathers',
        data=rfm_df.sort_values(by='frequency', ascending=False),
        palette=colors, hue='weathers', legend=False
    )
    plt.ylabel(None)
    plt.xlabel(None)
    plt.title('By Frequency (weathers)', loc='center', fontsize=18)
    plt.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)

fig = plt.figure(figsize=(15, 6))
sns.barplot(
    y='monetary', x='weathers',
    data=rfm_df.sort_values(by='monetary', ascending=False),
    palette=colors, hue='weathers', legend=False
)
plt.ylabel(None)
plt.xlabel(None)
plt.title('By Monetary (weathers)', loc='center', fontsize=18)
plt.tick_params(axis='x', labelsize=15)
st.pyplot(fig)
