lint:
	@flake8 --exclude="./build/" --ignore="E501"

publish:
	rm -r ./dist/*
	python3 setup.py sdist
	twine upload dist/*
