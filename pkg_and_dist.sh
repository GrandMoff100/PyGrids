python setup.py sdist
pip install twine -q -q
twine upload dist/* -u $user -p $passw
rm -rf build/ dist/ *.egg-info/