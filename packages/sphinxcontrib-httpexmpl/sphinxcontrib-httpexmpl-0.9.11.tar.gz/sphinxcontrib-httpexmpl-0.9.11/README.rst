sphinxcontrib-httpexmpl
=========================

.. image:: https://secure.travis-ci.org/collective/sphinxcontrib-httpexmpl.png
   :target: http://travis-ci.org/collective/sphinxcontrib-httpexmpl

.. image:: https://coveralls.io/repos/github/collective/sphinxcontrib-httpexmpl/badge.svg?branch=master
   :target: https://coveralls.io/github/collective/sphinxcontrib-httpexmpl?branch=master

.. image:: https://badge.fury.io/py/sphinxcontrib-httpexmpl.svg
   :target: https://badge.fury.io/py/sphinxcontrib-httpexmpl

.. image:: https://readthedocs.org/projects/sphinxcontrib-httpexmpl/badge/?version=latest
   :target: http://sphinxcontrib-httpexmpl.readthedocs.io/en/latest

sphinxcontrib-httpexmpl enhances `sphinxcontrib-httpdomain`_, a Sphinx domain extension for describing RESTful HTTP APIs in detail, with a simple call example directive. The new directive provided by this extension generates RESTful HTTP API call examples for different tools from a single HTTP request example.

The audience for this extension are developers and technical writes documenting their RESTful HTTP APIs. This extension has originally been developed for documenting `plone.restapi`_.

.. _sphinxcontrib-httpdomain: https://pythonhosted.org/sphinxcontrib-httpdomain/
.. _plone.restapi: http://plonerestapi.readthedocs.org/


Features
--------

* Directive for generating various RESTful HTTP API call examples from single HTTP request.

* Supported tools:

  - curl_
  - wget_
  - httpie_
  - python-requests_

.. _curl: https://curl.haxx.se/
.. _wget: https://www.gnu.org/software/wget/
.. _httpie: https://httpie.org/
.. _python-requests: http://docs.python-requests.org/


Examples
--------

This extension has been used at least in the following documentations:

* http://plonerestapi.readthedocs.org/
* http://sphinxcontrib-httpexmpl.readthedocs.org/
* https://guillotina.readthedocs.io/en/latest/


Documentation
-------------

Full documentation for end users can be found in the "docs" folder. It is also available online at http://sphinxcontrib-httpexmpl.readthedocs.org/


Installation
------------

Add sphinxcontrib-httpexmpl into requirements of your product documentation and into the configuration file of your Sphinx documentation next to sphincontrib-httpdomain as follows:

..  code:: python

    extensions = ['sphinxcontrib.httpdomain', 'sphinxcontrib.httpexmpl']


License
-------

The project is licensed under the GPLv2.
