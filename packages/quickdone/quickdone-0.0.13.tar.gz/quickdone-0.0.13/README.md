# Get Things Done Quickly!

### Usage
```bash
$ pip install quickdone
```
```python
>>> import quickdone as qd
```

fp() short for format_path(file_path)
```python
>>> qd.fp(r'C:\Users\user_name\Desktop\test.xlsx')
'C:/Users/user_name/Desktop/test.xlsx'
```

etc() short for excel_to_csv(input_path,output_path,input_enc,output_enc)
```python
>>> qd.etc(r'C:\Users\user_name\Desktop\test.xlsx',r'C:\Users\user_name\Desktop\test.csv')
```

### Packaging
```bash
$ python setup.py sdist bdist_wheel
$ twine upload dist/*
```

For more, see [python packaging-projects](https://packaging.python.org/tutorials/packaging-projects/) or [Packaging and distributing projects](https://packaging.python.org/guides/distributing-packages-using-setuptools/)