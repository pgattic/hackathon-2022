import PySimpleGUI as sg
import os
from analysis import *
from base64img import *

# For compiled version: close the splash screen before running the rest of the code
try:
	import pyi_splash
	pyi_splash.close()
except:
	print("Running with interpreter - No splash screen")


# Define Icons (gotta be in base64)


sg.theme('LightBlue')
dark_color = "#C0DBE5"


"""

	NOTE: Because of how the code is organized, all possible windows are structured as functions that invoke each other to call each other's opening

"""



# About Us Window
def about_window():
	layout = [
		[sg.Text("Home Care Analysis - 2022")],
		[sg.Text("Made with love by Team Fresh Meat")],
		[sg.Image(data=us_img)],
		[sg.Text("For Home Care Pulse")],
		[sg.Text("Usage:")],
		[sg.Text("Browse for the .csv file to be analyzed,")],
		[sg.Text("then export prediction data or select your")],
		[sg.Text("analysis options and see the charts!")],
	]
	window = sg.Window('About', layout, icon=info_icon, element_justification="center")
	# Event Loop to process "events" and get the "values" of the inputs
	while True:
		event, values = window.read()
		print(event)
		if event == sg.WIN_CLOSED or event == 'Done':
			break

	window.close()


# Main Front Window

def main_window():

	# Analysis Options (shows after file import)
	options_layout = [
		[sg.Checkbox("Prediction Analysis", key="p-analysis", default=True, background_color=dark_color)],
		[sg.Checkbox("Anomaly Detection", key="o-id", default=True, background_color=dark_color)],
		[sg.Text("Months to Predict:", background_color=dark_color), sg.Spin([i for i in range(0, 45)], key="months-spin", size=(4,None), initial_value=1, background_color="#E3F2FD")],
		[sg.Text("Accuracy:", background_color=dark_color), sg.Spin([i for i in range(0, 101)], key="accuracy-spin", size=(4,None), initial_value=90, pad=(0, 0), background_color="#E3F2FD"), sg.Text("%", background_color=dark_color)],
	]


	# Main App Layout
	layout = [
		[sg.Text('Browse to a ".csv" file'), sg.Button("", button_color="#E3F2FD", image_data=info_icon, size=(16,16),key="info")],
		[sg.Input(key='-FILE-', visible=False, enable_events=True), sg.FileBrowse(file_types=(("Comma Separated Values", "*.csv"),)), sg.Text("Selected File: none", key="file-selected")],

		[sg.Frame("Analysis Options:", key = "a-options", layout=options_layout, visible=False, background_color=dark_color, relief="flat")],

		[sg.Button('Display Plots', disabled = True, border_width = 0), sg.Button("Export Prediction Data as csv", key = "ex-csv", disabled = True)],
		[sg.Text("Ready to load data.", key="status")]
	]

	window = sg.Window("Home Care Analysis", layout, icon=app_icon, element_justification="center")

	def status(state):
		window["status"].update(state)

	# Event Loop
	while True:
		event, values = window.read()
		# print(f'New Event: "{event}"')
		# print(f'New Value: "{values}"')
		if event == sg.WIN_CLOSED or event=="Exit":
			break
		elif event == "info":
			about_window()
		elif event == "-FILE-":
			window["file-selected"].update(f"Selected File: {os.path.basename(values['-FILE-'])}")
			window["a-options"].Update(visible=True)
			window["Display Plots"].Update(disabled=False)
			window["ex-csv"].Update(disabled=False)
			status(f"Successfully loaded {os.path.basename(values['-FILE-'])}.")
		elif event == "Display Plots":
			analyze_data(values['-FILE-'],values["p-analysis"], int(values["accuracy-spin"])/100, values["months-spin"], values["o-id"])
		elif event == "ex-csv":
			status("Exporting...")
			data_predictions(values['-FILE-'], int(values["accuracy-spin"])/100, int(values["months-spin"]))
			status(f'Data saved to "output/data.csv".')

	window.close()


# Invoke main window
main_window()

