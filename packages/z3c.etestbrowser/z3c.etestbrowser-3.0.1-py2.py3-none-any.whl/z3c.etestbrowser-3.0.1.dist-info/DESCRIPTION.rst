=====================================
Extensions for the Zope 3 testbrowser
=====================================

This package is intended to provide extended versions of the Zope 3
testbrowser_. Especially those extensions that introduce dependencies to more
external products, like lxml.

.. _testbrowser: https://pypi.org/project/zope.testbrowser/

.. contents::

Extension: lxml-support
=======================

All HTML pages are parsed and provided as an element-tree.


Extended testbrowser
--------------------

This package provides some extensions to ``zope.testbrowser``.  These are not
included in the core because they have extra dependencies, such as ``lxml``.


Requirements
~~~~~~~~~~~~

 - lxml


etree support
~~~~~~~~~~~~~

The extended test browser allows parsing of the result of a request into an
etree using lxml (if the content type is text/html or text/xml).

This is useful to perform more detailed analysis of web pages using e.g. XPath
and related XML technologies.

Example:

  >>> from z3c.etestbrowser.testing import ExtendedTestBrowser
  >>> browser = ExtendedTestBrowser()
  >>> browser.open("http://localhost/")
  >>> print(browser.contents)
  <!DOCTYPE ...>
  ...
  </html>
  >>> browser.etree
  <Element html at ...>
  >>> browser.etree.xpath('//body')
  [<Element body at ...>]


Strict XML
++++++++++

It is possible to force the test browser to use the xml parser:

  >>> browser.xml_strict
  False
  >>> browser.xml_strict = True
  >>> browser.open("http://localhost/")
  >>> browser.etree
  <Element {http://www.w3.org/1999/xhtml}html at ...>
  >>> browser.etree.xpath(
  ...     '//html:body', namespaces={'html': 'http://www.w3.org/1999/xhtml'})
  [<Element {http://www.w3.org/1999/xhtml}body at ...>]

LXML unicode support
++++++++++++++++++++

A couple of variations of libxml2 might interpret UTF-8 encoded strings
incorrectly. We have a workaround for that. Let's have a look at a view that
contains a German umlaut:

  >>> browser.xml_strict = False
  >>> browser.open('http://localhost/lxml.html')
  >>> browser.etree.xpath("//span")[0].text == u'K\xfcgelblitz.'
  True

Invalid XML/HTML responses
++++++++++++++++++++++++++

Responses that contain a body with invalid XML/HTML will cause an error when
accessing the etree or normalized_contents attribute, but will load fine for
general TestBrowser use:

  >>> browser.open("http://localhost/empty.html")
  >>> browser.contents
  ''
  >>> browser.etree
  Traceback (most recent call last):
  ValueError: ...
  >>> browser.normalized_contents
  Traceback (most recent call last):
  ValueError: ...


HTML/XML normalization
~~~~~~~~~~~~~~~~~~~~~~

The extended test browser allows normalized output of HTML and XML which makes
testing examples with HTML or XML a bit easier when unimportant details like
whitespace are changing:

  >>> browser.open('http://localhost/funny.html')
  >>> print(browser.contents)
  <html>
    <head>
      <title>Foo</title>
  </head>
      <body>
            <h1>
        Title
      </h1>
          </body>
              </html>
  <BLANKLINE>

versus

  >>> print(browser.normalized_contents)
  <html>
    <head>
      <title>Foo</title>
    </head>
    <body>
      <h1>
        Title
      </h1>
    </body>
  </html>


Deprecated special support for zope.testbrowser.wsgi
----------------------------------------------------

There was also a variant in ``z3c.etestbrowser.wsgi`` which could be used for
the WSGI variant of ``zope.testbrowser``. It is no longer necessary because.
``z3c.etestbrowser.testing`` now speaks WSGI. It will be removed in the next
major release.

Example:

  >>> import z3c.etestbrowser.wsgi
  >>> browser = z3c.etestbrowser.wsgi.Browser(wsgi_app=wsgi_app)
  >>> browser.open("http://localhost/")
  >>> print(browser.contents)
  <!DOCTYPE ...>
  ...
  </html>
  >>> browser.etree
  <Element html at ...>
  >>> browser.etree.xpath('//body')
  [<Element body at ...>]



Using testbrowser on the internet
---------------------------------

The ``z3c.etestbrowser.browser`` module exposes an ``ExtendedTestBrowser``
class that simulates a web browser similar to Mozilla Firefox or IE.

    >>> from z3c.etestbrowser.browser import ExtendedTestBrowser
    >>> browser = ExtendedTestBrowser()

It can send arbitrary headers; this is helpful for setting the language value,
so that your tests format values the way you expect in your tests, if you rely
on zope.i18n locale-based formatting or a similar approach.

    >>> browser.addHeader('Accept-Language', 'en-US')

The browser can `open` web pages:

    >>> # This is tricky, since in Germany I am forwarded to google.de usually;
    >>> # The `ncr` forces to really go to google.com.
    >>> browser.open('http://google.com/ncr')
    Traceback (most recent call last):
    ...
    RobotExclusionError: HTTP Error 403: request disallowed by robots.txt

Oops!  Google doesn't let robots use their search engine.  Oh well.


=======
CHANGES
=======

3.0.1 (2019-03-05)
==================

- Fix deprecation declaration in ``.wsgi``.


3.0 (2019-03-04)
================

Backwards incompatible changes
------------------------------

- Add support for ``zope.testbrowser >= 5.0`` which speaks WSGI this requires
  tests to be updated to WSGI.

- Deprecate ``z3c.etestbrowser.wsgi`` which used to contain the WSGI variant
  as it is now the default.

- Drop the ``zope.app.testing`` extra introduced in version 2.0.0 as
  it dropped its special ``zope.testbrowser`` support.

- Drop ``.browser.ExtendedTestBrowser.pretty_print`` as its requirements are
  deprecated or even removed from Python's StdLib.

- Adapt the code to newer ``lxml`` versions which no longer raise an exception
  if the string to be parsed by ``lxml.etree`` is empty. We now raise a
  ``ValueError`` in this case.

Features
--------

- Add support for Python 3.6 up to 3.7.


2.0.1 (2015-11-09)
==================

- Fix `over_the_wire.txt`


2.0.0 (2011-10-13)
==================

- No longer depending on ``zope.app.wsgi`` but on ``zope.testbrowser`` >= 4.0
  for the WSGI flavor of testbrowser.

- Added a `zope.app.testing` extra. You should use this extra if you want to
  use the browser in ``z3c.etestbrowser.testing``. (The base testbrowser used
  there has been moved from ``zope.testbrowser`` to ``zope.app.testing`` in
  version 4.0.)

- Renamed ``z3c.etestbrowser.wsgi.ExtendedTestBrowser`` to ``Browser`` for
  equality with ``zope.testbrowser`` but kept ``ExtendedTestBrowser`` for
  backwards compatibility.

1.5.0 (2010-08-22)
==================

- Added ``z3c.etestbrowser.wsgi.ExtendedTestBrowser``, a variant that can be
  used when the test layer was set up using ``using
  zope.app.wsgi.testlayer``. see
  `Deprecated special support for zope.testbrowser.wsgi`_.


1.4.0 (2010-07-08)
==================

- Took ``zope.securitypolicy`` refactoring and ``zope.testing.doctest``
  deprecation into account.

- Added ``z3c.etestbrowser.browser.ExtendedTestBrowser``, a variant that
  speaks HTTP instead of directly talking to the publisher talks to the
  publisher, see `Using testbrowser on the internet`_.


1.3.1 (2010-01-18)
==================

- Added doctest to `long_description` to show up on pypi.

1.3.0 (2009-07-23)
==================

- Updgraded pacakge to lxml 2.2.

- Fixed bug with `normalized_contents` which would break the `open` function
  of test browser if content wasn't parsable as HTML/XML.

1.2.0 (2008-05-29)
==================

- Added `normalized_contents` attribute that reindents and normalizes the
  etree structure of a document and allows easier to read HTML/XML examples in
  doctests.


