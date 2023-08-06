# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['djangovue',
 'djangovue.examples.config',
 'djangovue.examples.example',
 'djangovue.examples.example.migrations',
 'djangovue.forms',
 'djangovue.templatetags',
 'djangovue.tests']

package_data = \
{'': ['*'], 'djangovue': ['static/djangovue/*']}

install_requires = \
['black==18.9b0',
 'bumpversion>=0.5.3,<0.6.0',
 'django-coverage-plugin>=1.6,<2.0',
 'django>=2.1,<3.0',
 'pytest-cov>=2.6,<3.0',
 'pytest-django>=3.4,<4.0',
 'pytest-sugar>=0.9.2,<0.10.0',
 'pytest>=4.3,<5.0',
 'twine>=1.13,<2.0']

setup_kwargs = {
    'name': 'djangovue',
    'version': '0.0.9',
    'description': 'A set of helper tags and form widgets for making django and vue play nicely.',
    'long_description': '# djangovue\n\n![Coverage](./coverage.svg)\n\nA set of helper tags and form widgets for making django and vue play nicely.\n\n# Installation\n\n```bash\npip install djangovue\n```\n\n# Tags Example\n\n```python\nclass IndexView(TemplateView):\n  template = \'index.html\'\n\n  def get_context_data(self, **kwargs):\n    context = super().get_context_data(**kwargs)\n    context[\'message\'] = \'Hello from Django\'\n    return context\n```\n\n\n```html\n{% load djangovue %}\n\n{% load_vuejs %}\n\n{% djangovue on %}\n  <div id="app">\n    <p>\n      {{ message }}\n  </p>\n  {% djangovue off %}\n    <p>\n    {{ message }}\n  </p>\n  {% enddjangovue off %}\n\n  </div>\n  \n  <script>\n    new Vue({\n      el: \'#app\',\n      data: {\n        message: \'Hello from Vue\'\n      }\n    });\n  </script>\n{% enddjangovue%}\n```\n\n# Widgets Example\n\n```python\nfrom django import forms\nfrom djangovue import widgets\n\n\nclass UserForm(forms.Form):\n    username = forms.CharField(\n        max_length=30,\n        widget=widgets.TextInput(\n            model="user.username",\n            modifier=widgets.TextInput.LAZY,\n            attrs={":disabled": "disable"},\n        ),\n    )\n    first_name = forms.CharField(\n        max_length=30,\n        widget=widgets.TextInput(\n            model="user.first_name", attrs={":disabled": "disable"}\n        ),\n    )\n    last_name = forms.CharField(\n        max_length=30,\n        widget=widgets.TextInput(\n            model="user.last_name", attrs={":disabled": "disable"}\n        ),\n    )\n    gender = forms.ChoiceField(\n        choices=[("male", "Male"), ("female", "Female")],\n        widget=widgets.RadioSelect(\n            attrs={"v-model": "user.gender", ":disabled": "disable"}\n        ),\n    )\n    disable = forms.BooleanField(\n        required=False, widget=widgets.CheckboxInput() # v-model will automatically be set to `disable`\n    )\n```\n\n# Development\n\nShould you wish to develop the library there are some helper functions within the Makefile to get you started.\n\n```bash\nmake install # Installs the project dependencies including the node modules required for the DjangoVue Vue plugin\nmake bundle # Transpiles and bundles the DjangoVue.ts file\nmake test # Runs tests\nmake black # Applies black formatting to the project\n```\n\nOnce installed run the following to view the examples:\n\n```bash\ncd djangovue/examples\npoetry run ./manage.py runserver\n```\n\nNote this project uses [Poetry](https://poetry.eustace.io/) for packaging and managing dependencies.\n',
    'author': 'Bradley Stuart Kirton',
    'author_email': 'bradleykirton@gmail.com',
    'url': 'https://gitlab.com/BradleyKirton/djangovue/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
