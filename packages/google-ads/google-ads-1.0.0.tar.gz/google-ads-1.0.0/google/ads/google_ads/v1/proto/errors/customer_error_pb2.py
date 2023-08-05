# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/errors/customer_error.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v1/proto/errors/customer_error.proto',
  package='google.ads.googleads.v1.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v1.errorsB\022CustomerErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v1/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V1.Errors\312\002\036Google\\Ads\\GoogleAds\\V1\\Errors\352\002\"Google::Ads::GoogleAds::V1::Errors'),
  serialized_pb=_b('\n9google/ads/googleads_v1/proto/errors/customer_error.proto\x12\x1egoogle.ads.googleads.v1.errors\x1a\x1cgoogle/api/annotations.proto\"x\n\x11\x43ustomerErrorEnum\"c\n\rCustomerError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x1c\n\x18STATUS_CHANGE_DISALLOWED\x10\x02\x12\x16\n\x12\x41\x43\x43OUNT_NOT_SET_UP\x10\x03\x42\xed\x01\n\"com.google.ads.googleads.v1.errorsB\x12\x43ustomerErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v1/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V1.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V1\\Errors\xea\x02\"Google::Ads::GoogleAds::V1::Errorsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_CUSTOMERERRORENUM_CUSTOMERERROR = _descriptor.EnumDescriptor(
  name='CustomerError',
  full_name='google.ads.googleads.v1.errors.CustomerErrorEnum.CustomerError',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STATUS_CHANGE_DISALLOWED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ACCOUNT_NOT_SET_UP', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=144,
  serialized_end=243,
)
_sym_db.RegisterEnumDescriptor(_CUSTOMERERRORENUM_CUSTOMERERROR)


_CUSTOMERERRORENUM = _descriptor.Descriptor(
  name='CustomerErrorEnum',
  full_name='google.ads.googleads.v1.errors.CustomerErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CUSTOMERERRORENUM_CUSTOMERERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=123,
  serialized_end=243,
)

_CUSTOMERERRORENUM_CUSTOMERERROR.containing_type = _CUSTOMERERRORENUM
DESCRIPTOR.message_types_by_name['CustomerErrorEnum'] = _CUSTOMERERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CustomerErrorEnum = _reflection.GeneratedProtocolMessageType('CustomerErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _CUSTOMERERRORENUM,
  __module__ = 'google.ads.googleads_v1.proto.errors.customer_error_pb2'
  ,
  __doc__ = """Container for enum describing possible customer errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.errors.CustomerErrorEnum)
  ))
_sym_db.RegisterMessage(CustomerErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
