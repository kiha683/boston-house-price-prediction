# -*- coding: utf-8 -*-
# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix
from sklearn.inspection import permutation_importance

from sklearn.linear_model import LinearRegression
regr = LinearRegression()
!pip install catboost
import catboost as cb
!pip install shap
import shap

from keras.models import Sequential
from keras.layers import Dropout
from keras.layers import Dense
from keras import models, layers

from sklearn.datasets import load_boston
boston = load_boston()

print(boston.keys())

print(boston.DESCR)

df = pd.DataFrame(boston.data,columns=boston.feature_names)                       #13 features
df = df
df['MEDV'] = boston.target                     #MEDV is our 
df.head()

df.isnull().sum()

sns.set(rc = {"figure.figsize":(10,10)})
sns.distplot (df["MEDV"])
plt.show()

correlation_matrix = df.corr().round(2)
sns.heatmap(data=correlation_matrix, annot = True)

plt.figure(figsize=(10, 5))
features = ["RM", "PTRATIO", "LSTAT"]
target = df["MEDV"]

for i, col in enumerate(features):
 plt.subplot(1, len(features) , i+1)
 # add data column into plot
 x = df[col]
 y = target
 plt.scatter(x, y, marker="o")
 plt.title(col)
 plt.xlabel(col)
 plt.ylabel("MEDV")

X = pd.DataFrame(np.c_[df["RM"], df["PTRATIO"], df["LSTAT"]], columns = ["RM", "PTRATIO", "LSTAT"])
Y = df["MEDV"]

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.1725, random_state=5)
print(X_train.shape) 
print(X_test.shape) 
print(Y_train.shape) 
print(Y_test.shape)

"""#Mutiple Regression"""

regr.fit(X_train,Y_train)
regr.predict(X_test)
print("R2", regr.score(X_test, Y_test))

fig = plt.figure(figsize=(10, 5))
Y_pred = regr.predict(X_test)
plt.scatter(Y_pred, Y_test)
plt.plot(Y_test,Y_test,'r')
plt.xlabel('Y_pred')
plt.ylabel('Y_test')
plt.show()

coeff_df = pd.DataFrame(regr.coef_, X_train.columns, columns=['Coefficient'])  
coeff_df

regr.intercept_

print("????????? : MEDIV = 21.493426383561197 + 4.140569 * RM ??? (-0.917104) * PTRATIO + (-0.639972) * LSTAT + error")

"""#Yandex Catboost"""

X, Y = load_boston(return_X_y = True)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.1725 , random_state=5)

train_dataset = cb.Pool(X_train, Y_train) 
test_dataset = cb.Pool(X_test, Y_test)

model = cb.CatBoostRegressor(loss_function = "RMSE")

grid = {'iterations': [100, 150, 200],'learning_rate': [0.03, 0.1]
        , 'depth': [2, 4, 6, 8], 'l2_leaf_reg': [0.2, 0.5, 1, 3]}
model.grid_search(grid, train_dataset)

pred = model.predict(X_test)
rmse = (np.sqrt(mean_squared_error(Y_test, pred)))
r2 = r2_score(Y_test, pred)
print("RMSE: {:.2f}".format(rmse))
print("R2: {:.2f}".format(r2))

fig = plt.figure(figsize=(10, 5))
plt.scatter(pred, Y_test)
plt.plot(Y_test,Y_test,'r')
plt.xlabel('Y_pred')
plt.ylabel('Y_test')
plt.show()

"""# DNN (???????????????????????????)"""

model = models.Sequential()

model.add(layers.Dense(50, input_shape=(X_train.shape[1],), activation='relu'))

model.add(layers.Dense(100, activation='relu'))

model.add(layers.Dense(50, activation='relu'))

model.add(layers.Dense(1))

model.summary()

model.compile(loss='mse', optimizer='adam',metrics = ['accuracy'])
model.fit(X_train, Y_train, epochs=500, validation_data=[X_test, Y_test], verbose=0)

loss_df = pd.DataFrame(model.history.history)
loss_df[['loss', 'val_loss']].plot(figsize=(10, 5))
plt.xlabel("Number of Epochs")
plt.ylabel("Loss")
plt.title("Training and Validation Loss Over Training Period", pad=12)

pred = model.predict(X_test)
rmse = (np.sqrt(mean_squared_error(Y_test, pred)))
r2 = r2_score(Y_test, pred)
print("RMSE: {:.2f}".format(rmse))
print("R2: {:.2f}".format(r2))

fig = plt.figure(figsize=(10, 5))
plt.scatter(pred, Y_test)
plt.plot(Y_test,Y_test,'r')
plt.xlabel('Y_pred')
plt.ylabel('Y_test')
plt.show()

"""# DNN (??????????????????????????????)"""

scaler = MinMaxScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

model = models.Sequential()

model.add(layers.Dense(50, input_shape=(X_train.shape[1],), activation='relu'))

model.add(layers.Dense(100, activation='relu'))

model.add(layers.Dense(50, activation='relu'))

model.add(layers.Dense(1))

model.summary()

model.compile(loss='mse', optimizer='adam',metrics = ['accuracy'])
model.fit(X_train, Y_train, epochs=500, validation_data=[X_test, Y_test], verbose=0)

loss_df = pd.DataFrame(model.history.history)
loss_df[['loss', 'val_loss']].plot(figsize=(10, 5))
plt.xlabel("Number of Epochs")
plt.ylabel("Loss")
plt.title("Training and Validation Loss Over Training Period", pad=12)

pred = model.predict(X_test)
rmse = (np.sqrt(mean_squared_error(Y_test, pred)))
r2 = r2_score(Y_test, pred)
print("RMSE: {:.2f}".format(rmse))
print("R2: {:.2f}".format(r2))

fig = plt.figure(figsize=(10, 5))
plt.scatter(pred, Y_test)
plt.plot(Y_test,Y_test,'r')
plt.xlabel('Y_pred')
plt.ylabel('Y_test')
plt.show()
