# Home Care Analysis

![App Icon](img/favicon.ico)

For Home Care Pulse

Repo for our hackathon October 2022 project

Made with ❤️ by Team Fresh Meat

![Team Photo](img/us.png)

# Requirements

## Python Packages: 

- PySimpleGUI
- Prophet
- webbrowser
- Altair
- Vega_Datasets

It should run in a Python environment just fine given these packages are installed. However, compiling is a little bit hacky, but it works!

## Compiling:

1. Make sure you have the Python package PyInstaller installed

2. Run `pyinstaller hc-analysis.spec` from within the repo's folder (theoretically works the same for Windows, Linux and macOS provided the prerequisites are all met)

> **Note:** You may get an error related to importing the Python libraries Prophet or vega-datasets, this is because PyInstaller is bad at recognizing imported Python libraries from the code. You can fix this by placing a copy of your installation of Prophet and vega-datasets in the code's "manual-imports" folder (usually found from `C:\Users\\[$USER]\AppData\Local\Programs\Python\Python310\Lib\site-packages` on Windows or `~/.local/lib/python3.10/site-packages/` on Linux)

# Contributors

- [Kent Barnhurst](https://github.com/OddPanda3) - Popcorn, Moral support, Ideas
- [Preston Corless](https://github.com/pgattic) - GUI, Compiling, Technical support
- [Bryant Van Orden](https://github.com/SupermanIsMeYes) - Implementation of data analysis libraries
- [Jack West](https://github.com/Jwesterner) - Project management
