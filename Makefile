test:
	nosetests --verbose

upload:
	python setup.py sdist upload

clean:
	find globlib -iname '*.pyc' -exec rm -f {} \;
	rm -fr globlib.egg-info dist

tag:
	@echo "[  ] tagging to version `cat VERSION.txt`..."
	git tag -a "v`cat VERSION.txt`" -m "released v`cat VERSION.txt`"

