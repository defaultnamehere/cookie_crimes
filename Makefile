src = $(wildcard *.c)
obj = $(src:.c=.o)


binary:
	pyinstaller -F cookie_crimes.py

clean:
	rm -rf dist/ build/ __pycache__ *.spec
