Welcome to Mailman Web's documentation!
=======================================

Mailman 3 web is an umbrella Django project that combines all the web
components of Mailman 3 into a single project that can be installed with a
single command and configured using a TOML configuration file.


=======
Install
=======

To install ``mailman-web`` using ``pip`` run the following command::

  $ pip install mailman-web


=====
Usage
=====

To run Django's development server, you can try::

  $ DJANGO_SETTINGS_MODULE=mailman_web.settings django-admin migrate
  $ DJANGO_SETTINGS_MODULE=mailman_web.settings django-admin runserver

========
Settings
========

Mailman Web can be customized using a `TOML configuration
<https://github.com/maxking/django-settings-toml>`_ file called
``mailman-web.toml``. The default locations where this configuration is
searched for (in order):

  - ``/etc/mailman-web.toml``
  - ``/etc/mailman3/mailman-web.toml``
  - ``./mailman-web.toml``

A basic configuration can look like this:

.. literalinclude:: mailman-web-example.toml

You can see a list of all the default configurations supported:

.. toctree::
   :maxdepth: 2

   settings

