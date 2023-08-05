default: clobber
	python setup.py sdist

package: default
	twine upload dist/*

clean:
	$(RM) *~

clobber: clean
	$(RM) -rf dist