# Python

# imports

import pandas
from prophet import *
import matplotlib
from vega_datasets import data as vega_data
import altair as alt
import webbrowser


# Connet and read data in CSV

load_csv = 'fake_data.csv'

data_file = pandas.read_csv(load_csv)

# change data from the date columb to become readable in the program

data_file['Date_of_Survey'] = pandas.to_datetime(data_file.Date_of_Survey)
print (data_file.dtypes)


# droping columbs that we aren't going to use

data_file.drop(['Last_Name', 'First_Name', 'Age', 'NPS_Scale', 'Date_of_Survey'], axis=1, inplace=True)
data_file.columns = ['y', 'ds']

# now we have two columbs which we need to work with prophet

data_file.head()