pip uninstall dismake -y
rm -rf dismake.egg-info
rm -rf dist
python setup.py sdist
twine upload dist/*
rm -rf dismake.egg-info
rm -rf dist