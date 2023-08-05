package: default
	git add .
	git commit -m "uploading to PyPi w/ twine"
	git push
	twine upload dist/*

default: clobber
	python setup.py sdist

clean:
	$(RM) *~

clobber: clean
	$(RM) -rf dist