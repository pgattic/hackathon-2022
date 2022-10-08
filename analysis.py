# Python

# imports
import os
import pandas
from prophet import Prophet
from vega_datasets import data as vega_data
import altair as alt
import webbrowser

def analyze_data(load_csv, prediction_analysis, accuracy_of_model, number_of_periods, technical_statistics, anomaly_chart ):
    accuracy_of_model = float(accuracy_of_model)
    number_of_periods = int(number_of_periods) 


# Connet and read data in CSV

#load_csv = 'hackathonrawdata2.csv'

    data_file = pandas.read_csv(load_csv)

# change data from the date columb to become readable in the program

    data_file['Date_of_Survey'] = pandas.to_datetime(data_file.Date_of_Survey)
#print (data_file.dtypes)
    data_file['ds'] = pandas.DatetimeIndex(data_file['Date_of_Survey'])


# droping columbs that we aren't going to use

    data_file.drop(['Last_Name', 'First_Name', 'Age', 'NPS', 'Date_of_Survey'], axis=1, inplace=True)
    data_file.columns = ['y', 'ds']

# now we have two columbs which we need to work with prophet

#print(data_file.head())

# building model: interval_width is what acuracy you want the interval to be in
# you can also add different parameters from Prophet like daily_seasonality=True  to make your prediction more accurate depending on your data

    model_formula = Prophet(interval_width=accuracy_of_model)
    model = model_formula.fit(data_file)

# the predicions of the data you can specify how many periods in advance you would like to predict with predict=
# you can specify what is the period 'M' month 'D' day 'Y' year

    future = model_formula.make_future_dataframe(periods=number_of_periods,freq='M')
    forecast = model_formula.predict(future)

# Show all analisis of the data and the predictions
# you can also start at the biggining with forecast.head()
    if technical_statistics:
        print(forecast.tail(number_of_periods))

# this clears up the data and only shows the preditions and dates

#print(forecast[['ds','yhat']]) 

# shaded blue is the bounding box of the predictions
# blue line is the predicitons 
# black dots are the real data points


    plot1 = model_formula.plot(forecast)
    if prediction_analysis:
        plot1.show("BRyant")
        
    


# interactive map

# code from https://towardsdatascience.com/anomaly-detection-time-series-4c661f6f165f

# Change this to match your model

    def fit_predict_model(data_file, interval_width = accuracy_of_model):
        m = Prophet()
        m = m.fit(data_file)
        forecast = m.predict(data_file)
        forecast['fact'] = data_file['y'].reset_index(drop = True)
        return forecast
    
    pred = fit_predict_model(data_file)

    def detect_anomalies(forecast):
        forecasted = forecast[['ds','trend', 'yhat', 'yhat_lower', 'yhat_upper', 'fact']].copy()
        #forecast['fact'] = df['y']

        forecasted['anomaly'] = 0
        forecasted.loc[forecasted['fact'] > forecasted['yhat_upper'], 'anomaly'] = 1
        forecasted.loc[forecasted['fact'] < forecasted['yhat_lower'], 'anomaly'] = -1

        #anomaly importances
        forecasted['importance'] = 0
        forecasted.loc[forecasted['anomaly'] ==1, 'importance'] = \
            (forecasted['fact'] - forecasted['yhat_upper'])/forecast['fact']
        forecasted.loc[forecasted['anomaly'] ==-1, 'importance'] = \
            (forecasted['yhat_lower'] - forecasted['fact'])/forecast['fact']
    
        return forecasted

    pred = detect_anomalies(pred)

    def plot_anomalies(forecasted):
        interval = alt.Chart(forecasted).mark_area(interpolate="basis", color = '#7FC97F').encode(
        x=alt.X('ds:T',  title ='date'),
        y='yhat_upper',
        y2='yhat_lower',
        tooltip=['ds', 'fact', 'yhat_lower', 'yhat_upper']
        ).interactive().properties(
            title='Anomaly Detection'
        )

        fact = alt.Chart(forecasted[forecasted.anomaly==0]).mark_circle(size=15, opacity=0.7, color = 'Black').encode(
            x='ds:T',
            y=alt.Y('fact', title='sales'),    
            tooltip=['ds', 'fact', 'yhat_lower', 'yhat_upper']
        ).interactive()

        anomalies = alt.Chart(forecasted[forecasted.anomaly!=0]).mark_circle(size=30, color = 'Red').encode(
            x='ds:T',
            y=alt.Y('fact', title='sales'),    
            tooltip=['ds', 'fact', 'yhat_lower', 'yhat_upper'],
            size = alt.Size( 'importance', legend=None)
        ).interactive()

        return alt.layer(interval, fact, anomalies)\
                .properties(width=870, height=450)\
                .configure_title(fontSize=20)
              
    chart= plot_anomalies(pred)

    chart.save('filename.html')

    if anomaly_chart:
        webbrowser.open_new_tab('filename.html')

def technical_data(load_csv, technical_statistics, accuracy_of_model, number_of_periods):
    accuracy_of_model = float(accuracy_of_model)
    number_of_periods = int(number_of_periods) 
    
    data_file = pandas.read_csv(load_csv)
    
    data_file['Date_of_Survey'] = pandas.to_datetime(data_file.Date_of_Survey)
    data_file['ds'] = pandas.DatetimeIndex(data_file['Date_of_Survey'])
    data_file.drop(['Last_Name', 'First_Name', 'Age', 'NPS', 'Date_of_Survey'], axis=1, inplace=True)
    data_file.columns = ['y', 'ds']
    
    model_formula = Prophet(interval_width=accuracy_of_model)
    model = model_formula.fit(data_file)
    
    future = model_formula.make_future_dataframe(periods=number_of_periods,freq='M')
    forecast = model_formula.predict(future)
    
    if technical_statistics:
        ds = forecast.tail(number_of_periods)
        ds.to_csv(index=False)
        os.makedirs('output', exist_ok=True)  
        ds.to_csv('output/data.csv')
        