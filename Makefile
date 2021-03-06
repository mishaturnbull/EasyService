.PHONY : main all clean preclean postclean

compiler = pyinstaller
target = src/coordinator.py
config = src/servicemanagerconfig.json
output = servicemanager

hiddenimports = --hidden-import functools

cflags = -F -y --specpath build --clean -n $(output) $(hiddenimports)

targetdir = /usr/local/bin

all: preclean main postclean

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
	chmod a+x $(targetdir)/servicemanager/$(output)
	cp $(config) $(targetdir)/servicemanager
	printf "#!/bin/bash\ncd $(targetdir)/servicemanager/\n./servicemanager" > $(targetdir)/servicemgr
	chmod a+x $(targetdir)/servicemgr

uninstall:
	-rm -rf $(targetdir)/servicemanager
	-rm -rf $(targetdir)/servicemgr
