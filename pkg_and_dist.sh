python setup.py sdist
pip install twine
twine upload dist/*
rm -rf build/ dist/ PyGrids.egg-info/