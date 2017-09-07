# encoding: utf-8

from __future__ import absolute_import

from schematics import types, models, schema
from google.protobuf.descriptor import FieldDescriptor

from proto_schematics import types as ptypes, models as pmodels


class MessageConverter(object):

    def __init__(self, module, message):
        self.module = module
        self.message = message
        self.model = None

    @property
    def name(self):
        return self.message.DESCRIPTOR.name

    def convert(self):
        self._build_model()

        for field in self._get_fields():
            converter = FieldConverter(self, field)
            self._add_field_to_model(converter.name, converter.convert())

        return self.model

    def _get_fields(self):
        return self.message.DESCRIPTOR.fields

    def _build_model(self):
        self.model = type(self.name, (pmodels.ProtobufMessageModel,), {})
        self.model._PROTOBUF_TYPE = self.message

    def _add_field_to_model(self, name, field):
        self.model._schema.append_field(schema.Field(name, field))
        setattr(self.model, name, models.FieldDescriptor(name))


class FieldConverter(object):

    PROTO_DESCRIPTOR_TYPES = {
        FieldDescriptor.TYPE_DOUBLE: types.FloatType,
        FieldDescriptor.TYPE_FLOAT: types.FloatType,
        FieldDescriptor.TYPE_INT64: types.IntType,
        FieldDescriptor.TYPE_UINT64: types.IntType,
        FieldDescriptor.TYPE_INT32: types.IntType,
        FieldDescriptor.TYPE_FIXED64: types.DecimalType,
        FieldDescriptor.TYPE_FIXED32: types.DecimalType,
        FieldDescriptor.TYPE_BOOL: types.BooleanType,
        FieldDescriptor.TYPE_STRING: types.StringType,
        FieldDescriptor.TYPE_GROUP: None,
        FieldDescriptor.TYPE_MESSAGE: None,
        FieldDescriptor.TYPE_BYTES: types.StringType,
        FieldDescriptor.TYPE_UINT32: types.IntType,
        FieldDescriptor.TYPE_ENUM: None,
        FieldDescriptor.TYPE_SFIXED32: types.DecimalType,
        FieldDescriptor.TYPE_SFIXED64: types.DecimalType,
        FieldDescriptor.TYPE_SINT32: types.IntType,
        FieldDescriptor.TYPE_SINT64: types.IntType,
    }

    PROTO_KNOWN_MESSAGES = {
        'google.protobuf.BoolValue': types.BooleanType,
        'google.protobuf.Timestamp': ptypes.UTCDateTimeType,
        'google.protobuf.Duration': ptypes.TimeDeltaType,
    }

    def __init__(self, message, descriptor):
        self.message = message
        self.descriptor = descriptor

    @property
    def name(self):
        return self.descriptor.name

    def convert(self):
        return self._get_type()

    @property
    def _is_repeated(self):
        # XXX: This seems unsafe
        return self.descriptor.default_value == []

    @property
    def _is_message(self):
        return bool(self.descriptor.message_type)

    @property
    def _is_enum(self):
        return bool(self.descriptor.enum_type)

    def _get_type(self):
        if self._is_repeated:
            return self._get_repeated_type()

        elif self._is_enum:
            return self._get_enum_type()

        elif self._is_message:
            return self._get_message_type()

        return self._get_native_type()

    def _get_native_type(self):
        return self.PROTO_DESCRIPTOR_TYPES[self.descriptor.type]()

    def _get_enum_type(self):
        # XXX: implement choices
        return types.StringType()

    def _get_message_type(self):
        known_type = self.PROTO_KNOWN_MESSAGES.get(self.descriptor.message_type.full_name)
        if known_type is not None:
            return known_type()

        return types.compound.ModelType(self._get_defined())

    def _get_repeated_type(self):
        if self._is_message:
            return types.compound.ListType(self._get_message_type())

        return types.compound.ListType(self._get_native_type())

    def _get_defined(self):
        return self.message.module._defs[self.descriptor.message_type.name]
