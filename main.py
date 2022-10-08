import PySimpleGUI as sg


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

	options_layout = [
		[sg.Checkbox("Prediction Analysis")],
		[sg.Checkbox("Outlier Identification")],
	]

	layout = [
		[sg.Menu(menu_def, tearoff=False)],
		[sg.Text('Browse to a ".csv" file')],
		[sg.Input(key='-FILE-', visible=False, enable_events=True), sg.FileBrowse(file_types=(("Comma Separated Values", "*.*"),)), sg.Text("Selected File: none", key="file-selected")],
		[sg.Frame("Analysis Options:", key="a-options", layout=options_layout, visible=False)],
		[sg.Button('Convert', disabled=True, tooltip="Select a file first!"), sg.Button('Done')],
		[sg.Text("Ready.", key="message")],
	]

	window = sg.Window("Main", layout, size=(800, 400))
	while True:
		event, values = window.read()
		print(f'New Event: "{event}"')
		if event == sg.WIN_CLOSED or event == 'Done' or event=="Exit":
			break
		elif event == "About...":
			about_window()
		elif event == "-FILE-":
			window["a-options"].Update(visible=True)
	window.close()
	

main_window()

