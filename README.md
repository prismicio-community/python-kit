## Python development kit for prismic.io

[![Latest Version](https://pypip.in/version/prismic/badge.svg)](https://pypi.python.org/pypi/prismic/)
[![Build Status](https://api.travis-ci.org/prismicio/python-kit.png)](https://travis-ci.org/prismicio/python-kit)

### Getting started

#### Install the kit for your project

Simply run:

```
pip install prismic
```

#### Get started with prismic.io

You can find out [how to get started with prismic.io](https://developers.prismic.io/documentation/UjBaQsuvzdIHvE4D/getting-started) on our [prismic.io developer's portal](https://developers.prismic.io/).

#### Get started using the kit

Also on our [prismic.io developer's portal](https://developers.prismic.io/), on top of our full documentation, you will:
 * get a thorough introduction of [how to use prismic.io kits](https://developers.prismic.io/documentation/UjBe8bGIJ3EKtgBZ/api-documentation#kits-and-helpers), including this one.
 * see [what else is available for Python](https://developers.prismic.io/technologies/UjBh78uvzeMJvE4o/python): starter projects, examples, ...


#### Kit's detailed documentation

You can find the documentation of the Python kit right here: http://prismic.readthedocs.org/en/latest/

Here is a basic example of use:
```python
>>> import prismic
>>> api = prismic.get("http://your-repo.prismic.io/api", "access_token")
>>> doc = api.get_by_uid("speculoos-macaron")
>>> doc.get_text("product.name")
u'Speculoos Macaron'
```

#### Using Memcached (or any other cache)

By default, the kit will use Shelve to cache the requests (a file-based cache from the standard library). It is recommended to use a cache server instead, for example Memcached.

You can pass a Memcached client to the `prismic.get` call:

```python
>>> import memcache
>>> api = prismic.get("http://your-lesbonneschoses.prismic.io/api", "access_token", memcache.Client(['127.0.0.1:11211']))
```

By duck typing you can pass any object that implement the `set` and `get` methods (see the `NoCache` object for the methods
to implement).

#### Using a Custom Request Handler

By default, the kit will use a request handler based on the popular package [requests](http://python-requests.org). If you, for some reason, wants to use a custom request handler,
 such as URLFetch (if you use Google AppEngine), for example. You can pass a function to the `prismic.get` call, this way:

 ```python
 >>> import prismic
 >>> import urllib2
 >>> def custom_request_handler(full_url):
 ...     r = urllib2.urlopen(full_url)
 ...     return r.getcode(), r.read(), r.info()
 ...
 >>> api = prismic.get("http://your-lesbonneschoses.prismic.io/api", "access_token", request_handler=custom_request_handler)
 ```

By duck typing you can pass any function that receives a URL and return a tuple containing status code, content and the headers of the response.

### Changelog

Need to see what changed, or to upgrade your kit? We keep our changelog on [this repository's "Releases" tab](https://github.com/prismicio/python-kit/releases).

### Contribute to the kit

Contribution is open to all developer levels, read our "[Contribute to the official kits](https://developers.prismic.io/documentation/UszOeAEAANUlwFpp/contribute-to-the-official-kits)" documentation to learn more.

#### Install the kit locally

This kit gets installed like any Python library.

*(Feel free to detail the proper steps for beginners by [submitting a pull request](https://developers.prismic.io/documentation/UszOeAEAANUlwFpp/contribute-to-the-official-kits).)*

#### Test

Please write tests for any bugfix or new feature.

If you find existing code that is not optimally tested and wish to make it better, we really appreciate it; but you should document it on its own branch and its own pull request.

You can launch tests using: `python setup.py test`.

#### Documentation

Please document any bugfix or new feature.

If you find existing code that is not optimally documented and wish to make it better, we really appreciate it; but you should document it on its own branch and its own pull request.

### Licence

This software is licensed under the Apache 2 license, quoted below.

Copyright 2013 Zengularity (http://www.zengularity.com).

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this project except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
