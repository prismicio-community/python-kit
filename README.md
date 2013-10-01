## Python development kit for prismic.io

### Installing

pip install git+https://github.com/prismicio/python-kit.git


### API documentation

Open docs/_build/html/index.html


### Example of use

```python
>>> import prismic
>>> api = prismic.get("http://your-lesbonneschoses.prismic.io/api", "access_token")
>>> form = api.form("everything")

>>> # Set the ref and the query to get all documents of type "product"
>>> form.ref(api.get_master()).query("""[[:d = any(document.type, ["product"])]]""")

>>> documents = form.submit()
>>> documents[0].get_text("product.name")
u'Speculoos Macaron'
```

### Sample applications

[python-django-starter](https://github.com/prismicio/python-django-starter) that shows the basic usage and [python-django-lesbonneschoses](https://github.com/prismicio/python-django-lesbonneschoses), a more advanced example.

### Licence

This software is licensed under the Apache 2 license, quoted below.

Copyright 2013 Zengularity (http://www.zengularity.com).

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this project except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.