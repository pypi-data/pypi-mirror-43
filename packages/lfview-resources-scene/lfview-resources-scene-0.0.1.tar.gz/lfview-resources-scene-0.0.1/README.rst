LFView Resources - Scene
************************************************************************

.. image:: https://img.shields.io/pypi/v/lfview-resources-scene.svg
    :target: https://pypi.org/project/lfview-resources-scene
.. image:: https://readthedocs.org/projects/lfview-resources-scene/badge/
    :target: http://lfview-resources-scene.readthedocs.io/en/latest/
.. image:: https://travis-ci.com/seequent/lfview-resources-scene.svg?branch=master
    :target: https://travis-ci.com/seequent/lfview-resources-scene
.. image:: https://codecov.io/gh/seequent/lfview-resources-scene/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/seequent/lfview-resources-scene
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/seequent/lfview-resources-scene/blob/master/LICENSE

.. warning::

    The LF View API and all associated Python client libraries are in
    **pre-release**. They are subject to change at any time, and
    backwards compatibility is not guaranteed.

Why?
----
This library exists to define scene resources in the
`LF View <https://lfview.com>`_ API. Resources include Slides,
Annotations, and Feedback as well as all the building blocks to
fully define a 3D scene.

Scope
-----
This library simply includes declarative definitions of scene resources.
It is built on `properties <https://propertiespy.readthedocs.io/en/latest/>`_ to
provide type-checking, validation, documentation, and serialization.
Very likely, these scene resources will be used in conjunction with
the `LF View API Python client <https://lfview.readthedocs.io/en/latest/>`_.

Installation
------------

You may install this library using
`pip <https://pip.pypa.io/en/stable/installing/>`_ with

.. code::

    pip install lfview-resources-scene

or from `Github <https://github.com/seequent/lfview-resources-scene>`_

.. code::

    git clone https://github.com/seequent/lfview-resources-scene.git
    cd lfview-resources-scene
    pip install -e .

You may also just install the LF View API Python client with

.. code::

    pip install lfview-api-client

After installing, you may access these resources with

.. code:: python

    from lfview.resources import scene

    slide = scene.Slide(...)
