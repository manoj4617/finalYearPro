#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense


# %matplotlib inline

rcParams['figure.figsize'] = 20,10

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0,1))
df = pd.read_csv("NSE-TATA.csv")
# print(df.head())

df["Date"] = pd.to_datetime(df.Date,format="%Y-%m-%d")
df.index = df["Date"]
# print(df.head())

# plt.figure(figsize=(16,8))
# plt.plot(df["Close"],Label="CLose Price History")

data = df.sort_index(ascending=True,axis=0)
# print("DATA",data.head())
new_dataset = pd.DataFrame(index=range(0,len(df)),columns=['Date','Close'])

for i in range(0,len(data)):
    new_dataset["Date"][i] = data['Date'][i]
    new_dataset["Close"][i] = data['Close'][i]

new_dataset.index = new_dataset.Date
new_dataset.drop("Date",axis=1,inplace=True)

final_dataset = new_dataset.values

train_data = final_dataset[0:987,:]
valid_data = final_dataset[987:,:]

scaler= MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(final_dataset)
x_train_data,y_train_data = [],[]

for i in range(60, len(train_data)):
    x_train_data.append(scaled_data[i-60:i,0])
    y_train_data.append(scaled_data[i,0])

# print("x train" ,  x_train_data)
# print("y train" , y_train_data)
x_train_data,y_train_data = np.array(x_train_data), np.array(y_train_data)
x_train_data=np.reshape(x_train_data,(x_train_data.shape[0],x_train_data.shape[1],1))

lstm_model = Sequential()
lstm_model.add(LSTM(units=50,return_sequences=True,input_shape=(x_train_data.shape[1],1)))
lstm_model.add(LSTM(units=50))
lstm_model.add(Dense(1))

lstm_model.compile(loss='mean_squared_error',optimizer='adam')
lstm_model.fit(x_train_data,y_train_data,epochs=5,batch_size=1,verbose=2)
input_data = new_dataset[len(new_dataset) - len(valid_data) - 60:].values
input_data = input_data.reshape(-1,1)
input_data = scaler.transform(input_data)

X_test = []
for i in range(60,input_data.shape[0]):
    X_test.append(input_data[i-60:i,0])
X_test =np.array(X_test)

X_test = np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))
prediction_close = lstm_model.predict(X_test)
prediction_close = scaler.inverse_transform(prediction_close)


train_data = new_dataset[:987]
valid_data = new_dataset[987:]
valid_data['Prediction'] = prediction_close
plt.plot(train_data["Close"])
plt.plot(valid_data[["Close","Prediction"]])

# %%
