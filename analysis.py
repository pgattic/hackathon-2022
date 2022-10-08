import os
import pandas
from prophet import Prophet
import altair as alt
import webbrowser


def analyze_data(csv_path, prediction_analysis, accuracy_of_model, number_of_periods, anomaly_chart ):
    accuracy_of_model = float(accuracy_of_model)
    number_of_periods = int(number_of_periods) 


# Connet and read data in CSV

    data_file = pandas.read_csv(csv_path)

# change data from the date columb to become readable in the program

    data_file['Date_of_Survey'] = pandas.to_datetime(data_file.Date_of_Survey)
    
#print (data_file.dtypes)

    data_file['ds'] = pandas.DatetimeIndex(data_file['Date_of_Survey'])


# dropping columns that we aren't going to use

    data_file.drop(['Last_Name', 'First_Name', 'Age', 'NPS', 'Date_of_Survey'], axis=1, inplace=True)
    data_file.columns = ['y', 'ds']

# now we have two columbs which we need to work with prophet


# shaded blue is the bounding box of the predictions
# blue line is the predicitons 
# black dots are the real data points

    if prediction_analysis:
        # building model: interval_width is what acuracy you want the interval to be in
        # you can also add different parameters from Prophet like daily_seasonality=True  to make your prediction more accurate depending on your data

        model_formula = Prophet(interval_width=accuracy_of_model)
        model = model_formula.fit(data_file)

        # the predicions of the data you can specify how many periods in advance you would like to predict with predict=
        # you can specify what is the period 'M' month 'D' day 'Y' year

        future = model_formula.make_future_dataframe(periods=number_of_periods,freq='M')
        forecast = model_formula.predict(future)
        fig = model.plot(forecast, xlabel='Date of Survey', ylabel='Rating')
        fig.gca().set_title("Prediction", size=12)
        fig.show()



# interactive map

    def fit_predict_model(data_file):
        model_formula = Prophet()
        model = model_formula.fit(data_file)
        forecast = model.predict(data_file)
        forecast['fact'] = data_file['y'].reset_index(drop = True)
        return forecast
    
    def detect_anomalies(forecast):
        forecasted = forecast[['ds','trend', 'yhat', 'yhat_lower', 'yhat_upper', 'fact']].copy()

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



    def plot_anomalies(forecasted):
        interval = alt.Chart(forecasted).mark_area(interpolate="basis", color = '#7FC97F').encode(
        x=alt.X('ds:T',  title ='Date of Survey'),
        y='yhat_upper',
        y2='yhat_lower',
        tooltip=['ds', 'fact', 'yhat_lower', 'yhat_upper']
        ).interactive().properties(
            title='Anomaly Detection'
        )

        fact = alt.Chart(forecasted[forecasted.anomaly==0]).mark_circle(size=15, opacity=0.7, color = 'Black').encode(
            x='ds:T',
            y=alt.Y('fact', title='Rating'),    
            tooltip=['ds', 'fact', 'yhat_lower', 'yhat_upper']
        ).interactive()

        anomalies = alt.Chart(forecasted[forecasted.anomaly!=0]).mark_circle(size=30, color = 'Red').encode(
            x='ds:T',
            y=alt.Y('fact', title='Rating'),    
            tooltip=['ds', 'fact', 'yhat_lower', 'yhat_upper'],
            size = alt.Size( 'importance', legend=None)
        ).interactive()

        return alt.layer(interval, fact, anomalies)\
                .properties(width=870, height=450)\
                .configure_title(fontSize=20)
              

# red dots are the outliers
# black is the actual data
# the blue is the projected range of the values

    if anomaly_chart:
        pred = fit_predict_model(data_file)
        pred = detect_anomalies(pred)
        chart = plot_anomalies(pred)
        chart.save('anomalies.html')
        webbrowser.open_new_tab('anomalies.html')

def data_predictions(csv_path, accuracy_of_model, number_of_periods):
    accuracy_of_model = float(accuracy_of_model)
    number_of_periods = int(number_of_periods) 
    
    data_file = pandas.read_csv(csv_path)
    
    data_file['Date_of_Survey'] = pandas.to_datetime(data_file.Date_of_Survey)
    data_file['ds'] = pandas.DatetimeIndex(data_file['Date_of_Survey'])
    data_file.drop(['Last_Name', 'First_Name', 'Age', 'NPS', 'Date_of_Survey'], axis=1, inplace=True)
    data_file.columns = ['y', 'ds']
    
    model_formula = Prophet(interval_width=accuracy_of_model)
    model = model_formula.fit(data_file)
    
    future = model_formula.make_future_dataframe(periods=number_of_periods,freq='M')
    forecast = model_formula.predict(future)
    
    # Output all analyses of the data and the predictions
    # you can also start at the biggining with forecast.head()
    ds = forecast.tail(number_of_periods)
    ds.to_csv(index=False)
    os.makedirs('output', exist_ok=True)  
    ds.to_csv('output/data.csv')
 
 
 # this is another HTML interactive chart
 
def prediction_html(csv_path, accuracy_of_model, number_of_periods, prediction_chart):
    
    accuracy_of_model = float(accuracy_of_model)
    number_of_periods = int(number_of_periods) 
    
    data_file = pandas.read_csv(csv_path)
    
    data_file['Date_of_Survey'] = pandas.to_datetime(data_file.Date_of_Survey)
    data_file['ds'] = pandas.DatetimeIndex(data_file['Date_of_Survey'])
    data_file.drop(['Last_Name', 'First_Name', 'Age', 'NPS', 'Date_of_Survey'], axis=1, inplace=True)
    data_file.columns = ['y', 'ds']
    
    model_formula = Prophet(interval_width=accuracy_of_model)
    model = model_formula.fit(data_file)
    
    future = model_formula.make_future_dataframe(periods=number_of_periods,freq='M')
    forecast = model_formula.predict(future)
    
    
    
    def fit_predict_model(data_file, interval_width = accuracy_of_model):
        forecast = model_formula.predict(future)
        forecast['fact'] = data_file['y'].reset_index(drop = True)
        return forecast
    
    interactive_pred = fit_predict_model(data_file)

    def detect(forecast):
        forecasted = forecast[['ds','trend', 'yhat', 'yhat_lower', 'yhat_upper', 'fact']].copy()
        #forecast['fact'] = df['y']

        forecasted['mean'] = 0
        forecasted.loc[forecasted['fact'] > forecasted['yhat_upper'], 'mean'] = 1
        forecasted.loc[forecasted['fact'] < forecasted['yhat_lower'], 'mean'] = -1

        return forecasted

    interactive_pred = detect(interactive_pred)

    def plot_a(forecasted):
        interval = alt.Chart(forecasted).mark_area(interpolate="basis", color = '#7FC97F').encode(
        x=alt.X('ds:T',  title ='Date of Survey'),
        y='yhat_upper',
        y2='yhat_lower',
        tooltip=['ds', 'fact', 'yhat_lower', 'yhat_upper']
        ).interactive().properties(
            title='Prediction'
        )

        fact = alt.Chart(forecasted).mark_circle(size=15, opacity=0.7, color = 'Black').encode(
            x='ds:T',
            y=alt.Y('fact', title='Rating'),    
            tooltip=['ds', 'fact', 'yhat_lower', 'yhat_upper']
        ).interactive()

        return alt.layer(interval, fact)\
                  .properties(width=870, height=450)\
                  .configure_title(fontSize=20)
    
    
    if prediction_chart:
        plot_a(interactive_pred)
        interactive_pred.save('anomalies.html')
        webbrowser.open_new_tab('anomalies.html')          