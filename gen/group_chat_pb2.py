# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: group_chat.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10group_chat.proto\"3\n\x04MIME\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0f\n\x07subtype\x18\x02 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\"x\n\x07Message\x12\x11\n\tsender_id\x18\x01 \x01(\x04\x12\x10\n\x08group_id\x18\x02 \x01(\x04\x12\x10\n\x08priority\x18\x03 \x01(\r\x12\x0c\n\x04text\x18\x04 \x01(\t\x12\x13\n\x04mime\x18\x05 \x01(\x0b\x32\x05.MIME\x12\x13\n\x0b\x63itation_id\x18\x06 \x01(\x04\"/\n\x08JoinInfo\x12\x11\n\tclient_id\x18\x01 \x01(\x04\x12\x10\n\x08group_id\x18\x02 \x01(\x04\"\x1e\n\nClientInfo\x12\x10\n\x08nickname\x18\x01 \x01(\t\"\'\n\x06Status\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0f\n\x07\x64\x65tails\x18\x02 \x01(\t\"Q\n\nInitStatus\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0e\n\x06new_id\x18\x02 \x01(\x04\x12\x14\n\x0cnew_group_id\x18\x03 \x01(\x04\x12\x0f\n\x07\x64\x65tails\x18\x04 \x01(\t\"2\n\x0cListenStatus\x12\x0f\n\x07\x63onfirm\x18\x01 \x01(\x08\x12\x11\n\tclient_id\x18\x02 \x01(\x04\x32\x9b\x01\n\tMessenger\x12\"\n\x04Init\x12\x0b.ClientInfo\x1a\x0b.InitStatus\"\x00\x12!\n\tJoinGroup\x12\t.JoinInfo\x1a\x07.Status\"\x00\x12\'\n\x06Listen\x12\r.ListenStatus\x1a\x08.Message\"\x00(\x01\x30\x01\x12\x1e\n\x07SendMsg\x12\x08.Message\x1a\x07.Status\"\x00\x62\x06proto3')



_MIME = DESCRIPTOR.message_types_by_name['MIME']
_MESSAGE = DESCRIPTOR.message_types_by_name['Message']
_JOININFO = DESCRIPTOR.message_types_by_name['JoinInfo']
_CLIENTINFO = DESCRIPTOR.message_types_by_name['ClientInfo']
_STATUS = DESCRIPTOR.message_types_by_name['Status']
_INITSTATUS = DESCRIPTOR.message_types_by_name['InitStatus']
_LISTENSTATUS = DESCRIPTOR.message_types_by_name['ListenStatus']
MIME = _reflection.GeneratedProtocolMessageType('MIME', (_message.Message,), {
  'DESCRIPTOR' : _MIME,
  '__module__' : 'group_chat_pb2'
  # @@protoc_insertion_point(class_scope:MIME)
  })
_sym_db.RegisterMessage(MIME)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGE,
  '__module__' : 'group_chat_pb2'
  # @@protoc_insertion_point(class_scope:Message)
  })
_sym_db.RegisterMessage(Message)

JoinInfo = _reflection.GeneratedProtocolMessageType('JoinInfo', (_message.Message,), {
  'DESCRIPTOR' : _JOININFO,
  '__module__' : 'group_chat_pb2'
  # @@protoc_insertion_point(class_scope:JoinInfo)
  })
_sym_db.RegisterMessage(JoinInfo)

ClientInfo = _reflection.GeneratedProtocolMessageType('ClientInfo', (_message.Message,), {
  'DESCRIPTOR' : _CLIENTINFO,
  '__module__' : 'group_chat_pb2'
  # @@protoc_insertion_point(class_scope:ClientInfo)
  })
_sym_db.RegisterMessage(ClientInfo)

Status = _reflection.GeneratedProtocolMessageType('Status', (_message.Message,), {
  'DESCRIPTOR' : _STATUS,
  '__module__' : 'group_chat_pb2'
  # @@protoc_insertion_point(class_scope:Status)
  })
_sym_db.RegisterMessage(Status)

InitStatus = _reflection.GeneratedProtocolMessageType('InitStatus', (_message.Message,), {
  'DESCRIPTOR' : _INITSTATUS,
  '__module__' : 'group_chat_pb2'
  # @@protoc_insertion_point(class_scope:InitStatus)
  })
_sym_db.RegisterMessage(InitStatus)

ListenStatus = _reflection.GeneratedProtocolMessageType('ListenStatus', (_message.Message,), {
  'DESCRIPTOR' : _LISTENSTATUS,
  '__module__' : 'group_chat_pb2'
  # @@protoc_insertion_point(class_scope:ListenStatus)
  })
_sym_db.RegisterMessage(ListenStatus)

_MESSENGER = DESCRIPTOR.services_by_name['Messenger']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MIME._serialized_start=20
  _MIME._serialized_end=71
  _MESSAGE._serialized_start=73
  _MESSAGE._serialized_end=193
  _JOININFO._serialized_start=195
  _JOININFO._serialized_end=242
  _CLIENTINFO._serialized_start=244
  _CLIENTINFO._serialized_end=274
  _STATUS._serialized_start=276
  _STATUS._serialized_end=315
  _INITSTATUS._serialized_start=317
  _INITSTATUS._serialized_end=398
  _LISTENSTATUS._serialized_start=400
  _LISTENSTATUS._serialized_end=450
  _MESSENGER._serialized_start=453
  _MESSENGER._serialized_end=608
# @@protoc_insertion_point(module_scope)
