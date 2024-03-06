#Import Packages/Library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

current_directory = os.getcwd()
print("Current Directory:", current_directory)

#Import dataset hour
#file_path = "D:\REXCEL\Bangkit\PROYEK 2\hour.csv"
hour_df = pd.read_csv("hour.csv")

print("Jumlah duplikasi: ", hour_df.duplicated().sum())

#rename kolom hour
hour_df = hour_df.rename(columns={'weathersit':'weather',
                       'instant':'id_customer',
                       'yr':'year',
                       'mnth':'month',
                       'hr':'hour',
                       'hum':'humidity',
                       'cnt':'count'})

# Convert 'dteday' column to datetime if not already
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# mengganti angka yang mewakili musim dengan label musim
season_string = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
hour_df['season'] = hour_df['season'].map(season_string)

# Convert 'dteday' column to datetime if not already
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Assuming season is defined as: 1 - spring, 2 - summer, 3 - fall, 4 - winter
def get_season(month):
    if month in [3, 4, 5]:
        return 1  # Spring
    elif month in [6, 7, 8]:
        return 2  # Summer
    elif month in [9, 10, 11]:
        return 3  # Fall
    else:
        return 4  # Winter

hour_df['season'] = hour_df['dteday'].dt.month.apply(get_season)

# Extract month from 'dteday'
hour_df['month'] = hour_df['dteday'].dt.month

# Rename bulan
bulan_map = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

hour_df['month'] = hour_df['month'].map(bulan_map)

# Jumlah peminjaman sepeda rata-rata berdasarkan bulan
avg_rentals_month = hour_df.groupby('month')['count'].mean()

# Analisis jumlah peminjaman sepeda berdasarkan musim
seasonly_rentals = hour_df.groupby('season')['count'].sum()

# Analisis jumlah peminjaman sepeda berdasarkan musim
monthly_rentals = hour_df.groupby('month')['count'].sum()

# Dashboard
st.header('Bike sharing pitch deck')

# Pengaruh musim terhadap peminjaman sepeda
st.subheader('Grafik Pengaruh Musim terhadap peminjaman sepeda')

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(seasonly_rentals.index, seasonly_rentals.values, marker='o', linestyle='-')

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_xticks(range(1, 5), ['Spring', 'Summer', 'Fall', 'Winter'])
ax.set_ylabel('Total Bike Rentals')
ax.set_xlabel('Season')
ax.set_title('Total Bike Rentals by Season')

 
st.pyplot(fig)

with st.expander("Description"):
    st.write(
        """Dari grafik pengaruh musim terhadap peminjaman sepeda, terkihat bahwa kenaikan
        jumlah peminjaman terjadi antara spring hingga summer. Dengan puncak peminjaman terbanyak
        terjadi pada summer. Urutan kedua berada pada fall (musim gugur), urutan ketiga ditempati oleh spring (musim semi),
        urutan keempat tingkat peminjaman terbanyak adalah musim dingin.
        """
    )

# Pengaruh tingkat peminjaman sepeda berdasarkan bulan
st.subheader('Pengaruh tingkat peminjaman sepeda berdasarkan bulan')

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(monthly_rentals.index, monthly_rentals.values, marker='o', linestyle='-')

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax.set_ylabel('Total Bike Rentals')
ax.set_xlabel('Month')
ax.set_title('Total Bike Rentals by Month')
 
st.pyplot(fig)

with st.expander("Description"):
    st.write(
        """Pada graik tersebut terlihat bahwa pada bulan januari, tingkat peminjaman sepeda begitu tinggi.
        Dari januari ke april, terlihat bahwa tingkat peminjaman sepeda menurun secara signiikan. Dari april-juni,
        tingkat peminjaman cenderung naik. lalu fluktuatif hingga beberapa bulan kedepan.
        """
    )

