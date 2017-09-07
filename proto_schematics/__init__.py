# encoding: utf-8

from __future__ import absolute_import

import importlib

from google.protobuf.internal.python_message import GeneratedProtocolMessageType

from proto_schematics.converters import MessageConverter


class ProtobufModule(object):

    def __init__(self, module_name):
        self.name = module_name
        self._defs = {}

    def _get_definitions(self):
        module = importlib.import_module(self.name)
        module_names = dir(module)
        module_defs = [getattr(module, name) for name in module_names]
        return module_defs

    def _get_messages(self):
        # XXX: include global enums
        return [d for d in self._get_definitions()
                if isinstance(d, GeneratedProtocolMessageType)]

    def import_schema(self):
        for message in self._get_messages():
            converter = MessageConverter(self, message)
            self._defs[converter.name] = converter.convert()

        return self._defs

    def meta_import(self):
        scope = globals()
        scope.update(self.import_schema())
