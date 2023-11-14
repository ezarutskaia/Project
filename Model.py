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

sql_query = "SELECT * FROM Accidents LIMIT 350000"
start_df = pd.read_sql(sql_query, connection)

# удаление NaN значений
df = start_df.dropna()

# подготовка фреймов предиктора х и целевой переменной у 
x = df[['Temperature','Humidity', 'Pressure', 'Visibility']].copy()
x['start_time'] = df['Start_Time'].dt.hour
y = df['Severity']

# разделение на обучающую и тестовую выборки
x_train, x_validation, y_train, y_validation = train_test_split(x, y, test_size=0.20, random_state=1)

# используемые модели
models = []
models.append(('knc', KNeighborsClassifier()))
models.append(('dtc', DecisionTreeClassifier()))

results = []
names = []

# выбор лучшей модели перебором 5 частей
for name, model in models:
	kfold = StratifiedKFold(n_splits=5, random_state=1, shuffle=True)
	cv_results = cross_val_score(model, x_train, y_train, cv=kfold, scoring='accuracy')
	results.append(cv_results)
	names.append(name)
	print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))
	
plt.boxplot(results, labels=names)
plt.title('Algorithm Comparison')
plt.show()

# обучение выбранной модели
dtc = DecisionTreeClassifier()
dtc.fit(x_train, y_train)
y_pred_knc = dtc.predict(x_validation)

# проверка точности модели
print('F1 Score on test data : ', f1_score(y_validation, dtc.predict(x_validation), average='weighted'))

# построение матрицы соответствия
knc_cm = confusion_matrix(y_validation, dtc.predict(x_validation))
sns.set(font_scale=1.5)
plt.figure(dpi=70)
sns.heatmap(knc_cm, annot=True, cmap='Greens', fmt='g')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()



