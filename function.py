import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from mysql.connector import connect
from sklearn.model_selection import train_test_split

# проверка допустимого интервала значений
def interval(n, min=False, max=False):

    if min!=False and n < min:
        raise ValueError('Значение меньше минимума', min)
    if max!=False and n > max:
        raise ValueError('Значение больше максимума', max)    
    return int(n)

# Построение модели
def Model():

    connection = connect(
        host="localhost",
        user="root",
        password="secret",
        database="Project",
        port="4306",
        )   
     
    sql_query = "SELECT * FROM Accidents LIMIT 55000"
    start_df = pd.read_sql(sql_query, connection)
    # удаление NaN значений
    df = start_df.dropna()
    # подготовка фреймов х и у 
    X = df[['Temperature','Humidity', 'Pressure', 'Visibility']].copy()
    X['Start_Time'] = df['Start_Time'].dt.hour
    y = df['Severity']
    # разделение на обучающую и тестовую выборки
    X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1)
    # обучение лучшей модели
    knc = KNeighborsClassifier()
    return knc.fit(X_train, Y_train)

def Prediction(knc, T, H, P, V, ST):

    data = pd.DataFrame(columns=['Temperature','Humidity', 'Pressure', 'Visibility', 'Start_Time'])
    data.loc[len(data.index)] = [T, H, P, V, ST]
    Predict = knc.predict(data)
    return Predict

#print(Prediction(Model(), 50, 30, 30, 15, 13))