Night Crawler
=============

Description
-----------

The NightCrawler is site crawling/spider tool to gather links at the given domain by walking through
the whole site and generating simple sitemap.

Limitations
-----------

This tools is just a demo. It's single-threaded script that walks every page it gets and it's
not optimized for speed.

The script sticks to the url provided and does not dive into subdomains of the given domain
even if encounters internal redirect like `example.com` -> `www.example.com`

Possible enhancements
---------------------

* Use multi-threading with thread pools
* Use generators to lower memory footprint and gain a bit more speed
* Make preliminary HEAD request to distinguish between text and binary files
* Check Content-Type and exclude files that are not HTMLs
* Add matchers and sitemap generators for additional sitemap flavour (images, videos, etc.)
* More tests (already included tests are only for the most critical classes)

Installation
------------

1. Requirements
~~~~~~~~~~~~~~~

1. Python >= 3.2
2. PIP

2a. Installation without virtualenv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Run the following command in shell:

.. code-block:: bash

  pip install NightCrawler

2b. Installation in virtualenv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the following command in shell:

.. code-block:: bash

  virtualenv .env
  . .env/bin/activate
  pip install NightCrawler

2c. Installation from source (development)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To install the package from source one have to create virtualenv after cloning the repository

.. code-block:: bash

  git clone https://github.com/szczad/NightCrawler.git
  cd NightCrawler
  virtualenv .env
  . .env/bin/activate
  pip install -e ./

3. (optional) Testing
~~~~~~~~~~~~~~~~~~~~~

When installed from sources in development mode the script can be tested with the following command

.. code-block:: bash

  . .env/bin/activate
  python setup.py test

Running the script
------------------

0. Help
~~~~~~~

.. code-block:: bash

    nightcrawler --help

1. Running the script installed globally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

  nightcrawler <url|domain>

2. Running the script installed in virtualenv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    <path_to_virtualenv>/bin/nightcrawler <url|domain>

or

.. code-block:: bash

    . .env/bin/activate
    nightcrawler <url|domain>
