DPATH=${CURDIR}

export DPATH
.PHONY:	build

build:
	rm dist/* && python setup.py sdist && pip install dist/*.tar.gz

