LFView Resources - Manifests
************************************************************************

.. image:: https://img.shields.io/pypi/v/lfview-resources-manifests.svg
    :target: https://pypi.org/project/lfview-resources-manifests
.. image:: https://readthedocs.org/projects/lfview-resources-manifests/badge/
    :target: http://lfview-resources-manifests.readthedocs.io/en/latest/
.. image:: https://travis-ci.com/seequent/lfview-resources-manifests.svg?branch=master
    :target: https://travis-ci.com/seequent/lfview-resources-manifests
.. image:: https://codecov.io/gh/seequent/lfview-resources-manifests/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/seequent/lfview-resources-manifests
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/seequent/lfview-resources-manifests/blob/master/LICENSE

.. warning::

    The LF View API and all associated Python client libraries are in
    **pre-release**. They are subject to change at any time, and
    backwards compatibility is not guaranteed.

What is lfview-resources-manifests?
-------------------------------------
This library exists to define manifest resources in the
`LF View <https://lfview.com>`_ API. For now, this only includes
View; you may use a View to selectively share your data with a wider
audience.

Scope
-----
This library simply includes declarative definitions of manifest resources.
It is built on `properties <https://propertiespy.readthedocs.io/en/latest/>`_ to
provide type-checking, validation, documentation, and serialization.
Very likely, these manifest resources will be used in conjunction with
the `LF View API Python client <https://lfview.readthedocs.io/en/latest/>`_.

Installation
------------

You may install this library using
`pip <https://pip.pypa.io/en/stable/installing/>`_ with

.. code::

    pip install seequent-resources-manifests

or from `Github <https://github.com/seequent/lfview-resources-manifests>`_

.. code::

    git clone https://github.com/seequent/lfview-resources-manifests.git
    cd lfview-resources-manifests
    pip install -e .

You may also just install the LF View API Python client with

.. code::

    pip install lfview-api-client

Either way, after installing, you may access the View resource with

.. code:: python

    from seequent.resources.manifests import View
