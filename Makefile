bin:
	@python -m PyInstaller --onefile --noconsole main.py

clean:
	@rm -rf build dist __pycache__
