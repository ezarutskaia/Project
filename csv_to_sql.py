import pandas as pd
import numpy as np
from mysql.connector import connect, Error

df = pd.read_csv("US_Accidents_March23.csv")

df = df.fillna(np.nan).replace([np.nan], [None])

df[['Amenity', 'Bump', 'Crossing', 'Give_Way', 'Junction', 'No_Exit', 'Railway', 'Roundabout', 'Station', 'Stop', 'Traffic_Calming', 'Traffic_Signal', 'Turning_Loop']] = df[['Amenity', 'Bump', 'Crossing', 'Give_Way', 'Junction', 'No_Exit', 'Railway', 'Roundabout', 'Station', 'Stop', 'Traffic_Calming', 'Traffic_Signal', 'Turning_Loop']].astype(np.int8).astype(str)

#print(df[['Amenity', 'Bump' , 'Crossing']])

#exit()

try:
    with connect(
        host="localhost",
        user="root",
        password="secret",
        database="Project",
        port="4306",
    ) as connection:

        with connection.cursor(buffered=True) as cursor:
            for ind in df.index:
                query = "INSERT INTO Accidents (ID, Severity, Start_Time, End_Time, Start_Lat, Start_Lng, Distance, Street, City, County, State, Zipcode, Country, Timezone, Airport_Code, Weather_Timestamp, Temperature, Wind_Chill, Humidity, Pressure, Visibility, Wind_Direction, Wind_Speed, Precipitation, Weather_Condition, Amenity, Bump, Crossing, Give_Way, Junction, No_Exit, Railway, Roundabout, Station, Stop, Traffic_Calming, Traffic_Signal, Turning_Loop, Sunrise_Sunset, Civil_Twilight, Nautical_Twilight, Astronomical_Twilight) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (
                    df['ID'][ind],
                    df['Severity'][ind].tolist(),
                    df['Start_Time'][ind],
                    df['End_Time'][ind], 
                    df['Start_Lat'][ind], 
                    df['Start_Lng'][ind],
                    df['Distance(mi)'][ind], 
                    df['Street'][ind], 
                    df['City'][ind], 
                    df['County'][ind], 
                    df['State'][ind], 
                    df['Zipcode'][ind], 
                    df['Country'][ind], 
                    df['Timezone'][ind], 
                    df['Airport_Code'][ind], 
                    df['Weather_Timestamp'][ind], 
                    df['Temperature(F)'][ind], 
                    df['Wind_Chill(F)'][ind], 
                    df['Humidity(%)'][ind], 
                    df['Pressure(in)'][ind], 
                    df['Visibility(mi)'][ind], 
                    df['Wind_Direction'][ind], 
                    df['Wind_Speed(mph)'][ind], 
                    df['Precipitation(in)'][ind], 
                    df['Weather_Condition'][ind], 
                    df['Amenity'][ind], 
                    df['Bump'][ind], 
                    df['Crossing'][ind], 
                    df['Give_Way'][ind], 
                    df['Junction'][ind], 
                    df['No_Exit'][ind], 
                    df['Railway'][ind], 
                    df['Roundabout'][ind], 
                    df['Station'][ind], 
                    df['Stop'][ind], 
                    df['Traffic_Calming'][ind], 
                    df['Traffic_Signal'][ind], 
                    df['Turning_Loop'][ind], 
                    df['Sunrise_Sunset'][ind], 
                    df['Civil_Twilight'][ind], 
                    df['Nautical_Twilight'][ind], 
                    df['Astronomical_Twilight'][ind]))
                connection.commit()

except Error as e:
    print('Error:',e)

