import PySimpleGUI as sg


# For compiled version: close the splash screen before running the rest of the code
try:
	import pyi_splash
	pyi_splash.close()
except: 
	print("Running with interpreter! No splash Screen!")

sg.theme('BlueMono')   # Add a touch of color
# All the stuff inside your window.


