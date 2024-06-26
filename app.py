import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import pandas_datareader as data
from datetime import date
from keras.models import load_model
import streamlit as st

start = '2010-01-01'
end = date.today()

st.title('Stock Price Prediction')


user_input = st.text_input('Enter Stock Ticker','AAPL')
df = yf.download(user_input,start,end)

#Describing the data
st.subheader('Data from 2010 - Today')
st.write(df.describe())

#visualization
st.subheader('Closing price vs Time Chart')
fig = plt.figure(figsize=(12,6))
plt.plot(df.Close)
# plt.legend()
# plt.show()
st.pyplot(fig)

#Moving Average of 100 days
st.subheader('Closing price vs Time Chart with 100MA')
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize=(12,6))
plt.plot(ma100, 'r', label = 'MA100')
plt.plot(df.Close, label =  'Closing Price')
plt.legend()
plt.show()
st.pyplot(fig)

#Moving Average of 200 days
st.subheader('Closing price vs Time Chart with 100MA & 200MA')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize=(12,6))
plt.plot(ma100, 'r', label = 'MA100')
plt.plot(ma200, 'g',label = 'MA200')
plt.plot(df.Close, label =  'Closing Price')
plt.legend()
plt.show()
st.pyplot(fig)

#Training and Testing Data
data_training = pd.DataFrame(df['Close'][0 : int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70) : int(len(df))])

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))

data_training_array = scaler.fit_transform(data_training)



#loading the model
model = load_model('keras_model.h5')

#Testing part
past_100_days = data_training.tail(100)
final_df = pd.concat([past_100_days,data_testing],ignore_index=True)
input_data = scaler.fit_transform(final_df)

x_test = []
y_test = []

for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i,0])
    
x_test, y_test = np.array(x_test), np.array(y_test)
y_predicted = model.predict(x_test)
scaler = scaler.scale_

scale_factor = 1/scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor

#Final Graph

st.subheader('Predictions vs Original')
fig2 = plt.figure(figsize=(12,6))
plt.plot(y_test, 'b', label = 'Original Price')
plt.plot(y_predicted, 'r', label = 'Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()
st.pyplot(fig2)