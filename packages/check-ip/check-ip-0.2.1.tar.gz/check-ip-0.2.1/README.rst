check-ip
========

*Check your public IP address and update DNS records on Cloudflare.*

.. image:: https://img.shields.io/github/license/samueljsb/check-ip.svg
    :target: license
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

Installation
------------

check-ip can be installed with pip::

    pip install check-ip

Usage
-----

::

    check-ip

The config file should take the following form

.. code-block:: yaml

    ---
    email: user@example.com
    api_key: <your Cloudflare API key>
    zone: example.com
    records:
    - www
    - server

You can specify a different file for configuration by passing it as an argument::

    check-ip my_config.yaml
