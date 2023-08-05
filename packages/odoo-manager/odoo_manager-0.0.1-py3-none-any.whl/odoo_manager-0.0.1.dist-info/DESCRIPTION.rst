# odoo-manager

## Setup

```
python3 -m pip install --user --upgrade setuptools wheel
python3 -m pip install --user --upgrade twine
```

## Distribution

### Generating Distribution

`python3 setup.py sdist bdist_wheel`

### Uploading Distribution

`python3 -m twine upload dist/*`



