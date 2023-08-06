# VAT Python utilities

## Using
Install:
```
pip install vat-utils
```

## Developing
Install dev requirements:
```
pip install -r requirements-dev.txt
```

Run tests with Tox:
```
tox
```

Build:
```
python setup.py sdist bdist_wheel
```

Publish to PyPi:
```
twine upload -r pypi dist/vat_utils-*
```

For more on publishing to PyPi, see https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/.
