# encoding: utf-8

from __future__ import absolute_import

from schematics import models
from google.protobuf.json_format import MessageToDict, ParseDict


class ProtobufMessageModel(models.Model):
    _PROTOBUF_TYPE = None

    def to_protobuf(self):
        return ParseDict(self.to_primitive(), self._PROTOBUF_TYPE())

    def import_message(self, message):
        return self.import_data(MessageToDict(message))
