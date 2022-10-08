import PySimpleGUI as sg
import os
from analysis import *
import pandas
from prophet import Prophet
from vega_datasets import data as vega_data
import altair as alt
import webbrowser

# For compiled version: close the splash screen before running the rest of the code
try:
	import pyi_splash
	pyi_splash.close()
except:
	print("Running with interpreter! No splash Screen!")

sg.theme('BlueMono')


# About Us Window

def about_window():
	layout = [
		[sg.Text("Made with love by the hackathon group Fresh Meat", justification='center')],
#		[sg.Image(source="img/icon-64x64.png")],
		[sg.Text("For Home Care Pulse", justification='center')],
	]
	window = sg.Window('About', layout)
	# Event Loop to process "events" and get the "values" of the inputs
	while True:
		event, values = window.read()
		print(event)
		if event == sg.WIN_CLOSED or event == 'Done':
			break

	window.close()


# Main Front Window

def main_window():
	menu_def = [
		["&File", ["&Import CSV", "E&xit"]],
		["&Help", ["&About..."]],
	]


	# Analysis Options (shows after file import)
	options_layout = [
		[sg.Checkbox("Prediction Analysis", key="p-analysis", default=True)],
		[sg.Checkbox("Outlier Identification", key="o-id", default=True)],
		[sg.Text("Months to Predict:"), sg.Spin([i for i in range(0, 45)], key="months-spin", size=(4,None), initial_value=1)],
		[sg.Text("Accuracy:"), sg.Spin([i for i in range(0, 101)], key="accuracy-spin", size=(4,None), initial_value=90, pad=(0, 0)), sg.Text("%")],
	]


	# Main App Layout
	layout = [
		[sg.Menu(menu_def, tearoff=False)],
		[sg.Text('Browse to a ".csv" file')],

		[sg.Input(key='-FILE-', visible=False, enable_events=True), sg.FileBrowse(file_types=(("Comma Separated Values", "*.csv"),)), sg.Text("Selected File: none", key="file-selected")],
		[sg.Frame("Analysis Options:", key="a-options", layout=options_layout, visible=False)], # MAKE VISIBLE False
		[sg.Button('Display Plots', disabled=True), sg.Button("Export Prediction Data as csv", key="ex-csv", disabled=True)],
		[sg.Text("Ready to load data.", key="status")]
	]

	window = sg.Window("Main", layout)

	def status(state):
		window["status"].update(state)

	# Event Loop
	while True:
		event, values = window.read()
		print(f'New Event: "{event}"')
		print(f'New Value: "{values}"')
		if event == sg.WIN_CLOSED or event=="Exit":
			break
		elif event == "About...":
			about_window()
		elif event == "-FILE-":
			window["file-selected"].update(f"Selected File: {os.path.basename(values['-FILE-'])}")
			window["a-options"].Update(visible=True)
			window["Display Plots"].Update(disabled=False)
			window["ex-csv"].Update(disabled=False)
			status(f"Successfully loaded {os.path.basename(values['-FILE-'])}.")
		elif event == "Display Plots":
			analyze_data(values['-FILE-'],values["p-analysis"], int(values["accuracy-spin"])/100, values["months-spin"], False, True)
		elif event == "ex-csv":
			status("Exporting...")
			technical_data(values['-FILE-'], True, int(values["accuracy-spin"])/100, int(values["months-spin"]))
			status(f'Data saved to "output/data.csv".')

	window.close()

#analyze_data(str("path/to/data.csv"), bool(prediction_analysis), int(months))
'''
def analyze_data(path, prediction_analysis, accuracy, months):
	print(f"Pathname: {path}\nPredicting? {prediction_analysis}\nHow many months? {months}\nAccuracy? {accuracy}")
'''


main_window()

