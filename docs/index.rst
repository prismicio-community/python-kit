.. Prismic documentation master file, created by
   sphinx-quickstart on Tue Oct  1 11:23:24 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Prismic's documentation!
===================================

Python development kit for prismic.io

Example of use::

    >>> import prismic
    >>> api = prismic.get("http://lesbonneschoses.prismic.io/api", "")
    >>> form = api.form("everything")

    >>> # Set the ref and the query to get all documents of type "product"
    >>> form.ref(api.get_master()).query("""[[:d = any(document.type, ["product"])]]""")

    >>> documents = form.submit()
    >>> documents[0].get_text("product.name")
    u'Speculoos Macaron'



Prismic API:

.. toctree::
   :maxdepth: 2

   prismic

To activate debugging::

    >>> import logging
    >>> logging.basicConfig(level=logging.DEBUG)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

