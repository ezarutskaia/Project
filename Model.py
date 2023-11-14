import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mysql.connector import connect
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import  confusion_matrix, f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

connection =  connect(
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
'''
models = []
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))

results = []
names = []
# выбор лучшей модели перебором 5 частей

for name, model in models:
	kfold = StratifiedKFold(n_splits=5, random_state=1, shuffle=True)
	cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
	results.append(cv_results)
	names.append(name)
	print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))
	
plt.boxplot(results, labels=names)
plt.title('Algorithm Comparison')
plt.show()
'''
knc = KNeighborsClassifier()
knc.fit(X_train, Y_train)
y_pred_knc = knc.predict(X_validation)

#print('F1 Score on test data : ', f1_score(Y_validation, knc.predict(X_validation), average='weighted'))

knc_cm = confusion_matrix(Y_validation, knc.predict(X_validation))
sns.set(font_scale=1.5)
plt.figure(dpi=70)
sns.heatmap(knc_cm, annot=True, cmap='Greens', fmt='g')
plt.xlabel('Predicted')
plt.ylabel('Actual')
#plt.show()

def Prediction(T, H, P, V, ST):
        data = pd.DataFrame(columns=['Temperature','Humidity', 'Pressure', 'Visibility', 'Start_Time'])
        data.loc[len(data.index)] = [T, H, P, V, ST]
        Predict = knc.predict(data)
        return Predict

#print(Prediction(50, 30, 30, 15, 13))

def numerator(n, min=False, max=False):
    #tp = type(n)
    if min!=False and n < min:
        raise ValueError('Значение меньше минимума', min)
    if max!=False and n > max:
        raise ValueError('Значение больше максимума', max)    
    return int(n)

