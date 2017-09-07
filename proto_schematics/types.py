# encoding: utf-8

from __future__ import absolute_import

from datetime import timedelta

from schematics import types, exceptions


class TimeDeltaType(types.BaseType):

    def __init__(self, **kwargs):
        super(TimeDeltaType, self).__init__(**kwargs)

    def validate(self, value, context=None):
        try:
            if isinstance(value, str):
                value = float(value[:-1])
        except:
            raise exceptions.ValidationError()

        try:
            if isinstance(value, float):
                value = timedelta(seconds=value)
        except:
            raise exceptions.ValidationError()

        return value

    def to_native(self, value, context=None):
        return self.validate(value)

    def to_primitive(self, value, context=None):
        return "{}s".format(value.total_seconds())


class UTCDateTimeType(types.DateTimeType):

    def __init__(self, **kwargs):
        kwargs.update(
            convert_tz=True,
        )
        super(UTCDateTimeType, self).__init__(**kwargs)
