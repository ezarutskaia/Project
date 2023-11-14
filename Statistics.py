import pandas as pd
import numpy as np
from mysql.connector import connect
import matplotlib.pyplot as plt
import seaborn as sns

connection =  connect(
    host="localhost",
    user="root",
    password="secret",
    database="Project",
    port="4306",
)

# получение данных из SQL
sql_query = "SELECT * FROM Accidents LIMIT 350000"
start_df = pd.read_sql(sql_query, connection)

# новый df для удобной работы со временем
df = pd.DataFrame(columns=['id', 'hour', 'day_week', 'severity'])
df['id'] = start_df['ID']
df['hour'] = start_df['Start_Time'].dt.hour
df['day_week'] = start_df['Start_Time'].dt.day_name()
df['severity'] = start_df['Severity']

# датафреймы для группировки и подсчёта количества аварий
grouped_hour = df.groupby('hour').size().reset_index(name='qty')
grouped_day = df.groupby('day_week').size().reset_index(name='qty')

# расположение дней недели на осях в нужном порядке
day_ordered = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
x1_Idx = np.where(day_ordered == np.expand_dims(df['day_week'],-1))[1]
x2_Idx = np.where(day_ordered == np.expand_dims(grouped_day['day_week'],-1))[1]

plt.subplot(221)
plt.stem(df['hour'], df['severity'])
plt.title('Severity and number of accidents per day')
plt.ylabel('severity')
plt.subplot(222)
plt.stem(x1_Idx, df['severity'])
plt.xticks(np.arange(7),day_ordered)
plt.title('Severity and number of accidents per week')
plt.ylabel('severity')
plt.subplot(223)
plt.plot(grouped_hour['hour'], grouped_hour['qty'])
plt.ylabel('number')
plt.subplot(224)
plt.stem(x2_Idx, grouped_day['qty'])
plt.xticks(np.arange(7),day_ordered)
plt.ylabel('number')
plt.show()

# группировка и подсчёт кличества аварий для погодных условий
grouped_temp = start_df.groupby('Temperature').size().reset_index(name='qty')
temp_sum = grouped_temp['qty'].sum()
grouped_temp['fraction'] = grouped_temp['qty'] / temp_sum

grouped_hum = start_df.groupby('Humidity').size().reset_index(name='qty')
hum_sum = grouped_hum['qty'].sum()
grouped_hum['fraction'] = grouped_hum['qty'] / hum_sum

grouped_pres = start_df.groupby('Pressure').size().reset_index(name='qty')
pres_sum = grouped_pres['qty'].sum()
grouped_pres['fraction'] = grouped_pres['qty'] / pres_sum

grouped_vis = start_df.groupby('Visibility').size().reset_index(name='qty')
vis_sum = grouped_vis['qty'].sum()
grouped_vis['fraction'] = grouped_vis['qty'] / vis_sum

plt.subplot(221)
plt.stem(grouped_temp['Temperature'], grouped_temp['qty'])
plt.xlabel('temperature')
plt.subplot(222)
plt.stem(grouped_hum['Humidity'], grouped_hum['qty'])
plt.xlabel('humidity')
plt.subplot(223)
plt.plot(grouped_pres['Pressure'], grouped_pres['qty'])
plt.xlabel('pressure')
plt.subplot(224)
plt.plot(grouped_vis['Visibility'], grouped_vis['qty'])
plt.xlabel('visibility')
plt.show()

# создание матрицы корреляции
correlation_df = start_df[['Temperature','Humidity', 'Pressure', 'Visibility']]. copy ()
correlation_matrix = correlation_df.corr()
plt.figure(figsize=(10, 8))  
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation map')
plt.show()