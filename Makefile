.PHONY : main all clean preclean postclean

compiler = pyinstaller
target = src/coordinator.py
config = src/servicemanagerconfig.json
output = servicemanager

hiddenimports = --hidden-import functools

cflags = -F -y --specpath build --clean -n $(outout) $(hiddenimports)

targetdir = /usr/local/bin

clean: preclean postclean

preclean:
	-rm -rf dist
	-rm -rf src/*.pyc
	-rm -rf __pycache__

postclean:
	-rm -rf build
	-rm -rf src/*.pyc

main:
	$(compiler) $(cflags) $(target)

install:
	-mkdir $(targetdir)/servicemanager
	cp dist/$(output) $(targetdir)/servicemanager
	chmod a+x $(targetdir)/servicemanager
	cp $(config) $(targetdir)/servicemanager

uninstall:
	-rm -rf $(targetdir)/servicemanager
