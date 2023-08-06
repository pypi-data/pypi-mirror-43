<!--
https://pypi.org/project/readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/django-replace.svg?longCache=True)](https://pypi.org/project/django-replace/)

#### Installation
```bash
$ [sudo] pip install django-replace
```

#### Examples
`settings.py`
```python
>>> INSTALLED_APPS = [
    'django_replace'
    ...
]
```

`template.html`
```html
{% load replace %}

{{ value|replace:",search,replace" }}
```

<p align="center">
    <a href="https://pypi.org/project/readme-generator/">readme-generator</a>
</p>