pip uninstall dismake -y
python setup.py sdist
twine upload dist/*
rm -rf dismake-egg-info
rm -rf dist