<!--
https://pypi.org/project/readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/writable-property.svg?longCache=True)](https://pypi.org/project/writable-property/)
[![](https://img.shields.io/pypi/v/writable-property.svg?maxAge=3600)](https://pypi.org/project/writable-property/)
[![Travis](https://api.travis-ci.org/looking-for-a-job/writable-property.py.svg?branch=master)](https://travis-ci.org/looking-for-a-job/writable-property.py/)

#### Installation
```bash
$ [sudo] pip install writable-property
```

#### Classes
class|`__doc__`
-|-
`writable_property.writable_property` |writable property class

#### Examples
```python
>>> from writable_property import writable_property

>>> class Class:
    @writable_property
    def prop(self):
        return "value"

>>> obj = Class()
>>> obj.prop
"value"

>>> obj.prop = "new"
>>> obj.prop
"new"
```

<p align="center">
    <a href="https://pypi.org/project/readme-generator/">readme-generator</a>
</p>