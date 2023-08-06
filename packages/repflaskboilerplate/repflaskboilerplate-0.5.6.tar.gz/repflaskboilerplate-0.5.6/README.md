### how to build me
- install setuptools and twine
- change the version number in setup.py
- python setup.py sdist bdist_wheel
- python -m twine upload --skip-existing dist/*
- ryans pypi

### how to import me
- add repflaskboilerplate to requirements.txt

