Proto Schematics
================

*Making Protobuf messages as cute as Python.*


Motivation
----------

Protobuf and gRPC are great when it comes to high performance schema aware APIs,
but when Google designed Protobuf, it didn't tried to make the generated code
idiomatic in Python, which brings a problem when exporting messages outside
iterface modules.

Schematics is a cute and pythonic schema library. Why not join both?


Installing
----------

Using pip::

    pip install proto_schamatics


Examples
--------

Inspecting a module is as simple as:

.. code:: python

    from proto_schematics import ProtobufModule

    models = ProtobufModule('my.protobuf.lib').import_schema()
    MySchamticsModel = models['ProtobufMessageName']

You can also do it on a lazy lint unfriendly way:

.. code:: python

    from proto_schematics import ProtobufModule
    ProtobufModule('my.protobuf.lib').meta_import()

    from protobuf_schematics import ProtobufMessageName as MySchematicsModel


Supports
--------

* Datetimes as native Python
* Duration as TimeDeltas
* Wrappers as native nullable types
