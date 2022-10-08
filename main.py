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
	print("Running with interpreter - No splash screen")

sg.theme('LightBlue')

app_icon = b"iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAAS1BMVEXm5uZ2QprlsTUAAACffraAUKHlw3Lk4+TlvV/lszrDss63ocbDw8Pl2sGzs7OVcK/l1a2FWKXm0qKenp6UlJTlyol7e3vlv2RYWFh6/RVIAAABGUlEQVRYw+3SS44CMQwE0IrTDMz/P8P9T4p6gcp0HOw4O0TtuqV6iuPgnpuPnJPt3wG8OkBqCyJzAD9yAL9ygEhW2HiSA0QlA8gE8L/tywPaPJfSEwA8inuCssYGov01iw14dQKlvBuAVyewneMgm/z2+zp7HsEfnoCOCQBRgIRbJ2AT6unEAaa5hKjAEAgqvuCPtDRTmPHvhAKGgb25zjhgP6nsowRsIryITzCDffAILREZnkBLHPzTowPgawVC/ScN6HwE+jv1B8Fc9hPATg+QAaD6IeCnK/DzilBrRUdAAKhrYAtwAAowBYSBIzqJjfAythU2eYPDAEf/Zj8DVMT6CwHV1xscu0SO/sZ+OOxPZb7/NwvgJnMCQwkIBRnsbfoAAAAASUVORK5CYII="

info_icon = b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAABd1BMVEUAAABkqt0LcrMZeb0OcbUIZ68CX6F4vuUGYKQOcbd1wuyT0PN3w+weg8Gp3vpRqNlDndMggsCU0O6r3/ZQp9lHn9FcsN84ls3L6fiFyOtcsN84lcwEWZmAxesDW599xOwPc7Z1weVmueZ2v+QPcLYujcaLyunf8flptuMYebwHTIgvjskJa6wXertqt+QFKlBlptMogL9ruOHO7Pkogb8MVJIAAAF1wekFaLBGodY5mM8rjccXebsPcbf5//+O0fOFyu1ru+ZpuuVDn9Wc2PfG5PGR0u+Cye13w+qJxeZhtOFfs+FTqds1lc4wj8kggsH8/v7i8vea1vaR0PLN5PGCyvFou+hZsuOBvuBcsd9OqNuGutpPqdlGmsw4lswqisYihMPy+/3x9/rv9vrs9Pjn8/ij2vbA4POy2/GY0vGm1u6z2euhyuZvveV1veSIvuB3u99Uqt1Tq9uDuddWqtdLotZBn9Q8l81GkscjhcMgfrwmfLshe7uj7mZLAAAAN3RSTlMADAb+/uXGg2X68u7t7ezr6ufi4dza0crBwb+5sayloZeUj4yLhYKBfn5+dW9tOTAuLCsqIBUF7K+CWQAAAPBJREFUGNMlyOVig0AQBOBNGqu7u7sL5Y5ACe5xt7q7y8P3IN/+2JkB1+7iUG/PcHgLGnwLHRdiUhSTrbM+r09yHCfLqWs5xY27SzijHBE3Z5KiZKYBdtooilJV9Sp+SULLBixlYzy5B0275/lYdgZGcgXD0PPpE0nXjUJuAPqKRfPlSbtlJfPZLJc7oV8QBPr97Tyep2la+OiCUcuqIvTIJmiEUNUahFWMsW2n2bvKp41xbR72up36d+WUfS3V6o7Tvg2w3sQwX8eJ0g/5zDIA+OeaA9HfvygRmPKDu0SCh57gGume/chEKDS2snlA8j80CzZ9UaG16wAAAABJRU5ErkJggg=="

dark_color = "#C0DBE5"

# About Us Window

def about_window():
	layout = [
		[sg.Text("2022 - Made with love by Team Fresh Meat")],
		[sg.Image(source="img/us.png")],
		[sg.Text("For Home Care Pulse")],
		[sg.Text("Usage:")],
		[sg.Text("Browse for the .csv file to be analyzed")],
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
		[sg.Frame("Analysis Options:", key="a-options", layout=options_layout, visible=False, background_color=dark_color, relief="flat")], # MAKE VISIBLE False
		[sg.Button('Display Plots', disabled=True, border_width = 0), sg.Button("Export Prediction Data as csv", key="ex-csv", disabled=True)],
		[sg.Text("Ready to load data.", key="status")]
	]

	window = sg.Window("Main", layout, icon=app_icon, element_justification="center")

	def status(state):
		window["status"].update(state)

	# Event Loop
	while True:
		event, values = window.read()
		print(f'New Event: "{event}"')
		print(f'New Value: "{values}"')
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
			analyze_data(values['-FILE-'],values["p-analysis"], int(values["accuracy-spin"])/100, values["months-spin"], False, values["o-id"])
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

