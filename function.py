import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from mysql.connector import connect
from sklearn.model_selection import train_test_split

# проверка допустимого интервала значений
def interval(n, min=False, max=False):
    if min!=False and n < min:
        raise ValueError('Значение меньше минимума', min)
    if max!=False and n > max:
        raise ValueError('Значение больше максимума', max)    
    return int(n)

# построение модели
def model():
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
    x = df[['Temperature','Humidity', 'Pressure', 'Visibility']].copy()
    x['Start_Time'] = df['Start_Time'].dt.hour
    y = df['Severity']
    # разделение на обучающую и тестовую выборки
    x_train, x_validation, y_train, y_validation = train_test_split(x, y, test_size=0.20, random_state=1)
    # обучение лучшей модели
    dtc = DecisionTreeClassifier()
    return dtc.fit(x_train, y_train)

def prediction(dtc, t, h, p, v, st):
    data = pd.DataFrame(columns=['Temperature','Humidity', 'Pressure', 'Visibility', 'Start_Time'])
    data.loc[len(data.index)] = [t, h, p, v, st]
    predict = dtc.predict(data)
    return predict