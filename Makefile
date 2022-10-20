bin:
	@python -m PyInstaller hc-analysis.spec

clean:
	@rm -rf build dist __pycache__
