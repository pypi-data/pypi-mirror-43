# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/errors/range_error.proto

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
  name='google/ads/googleads_v1/proto/errors/range_error.proto',
  package='google.ads.googleads.v1.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v1.errorsB\017RangeErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v1/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V1.Errors\312\002\036Google\\Ads\\GoogleAds\\V1\\Errors\352\002\"Google::Ads::GoogleAds::V1::Errors'),
  serialized_pb=_b('\n6google/ads/googleads_v1/proto/errors/range_error.proto\x12\x1egoogle.ads.googleads.v1.errors\x1a\x1cgoogle/api/annotations.proto\"W\n\x0eRangeErrorEnum\"E\n\nRangeError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0b\n\x07TOO_LOW\x10\x02\x12\x0c\n\x08TOO_HIGH\x10\x03\x42\xea\x01\n\"com.google.ads.googleads.v1.errorsB\x0fRangeErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v1/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V1.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V1\\Errors\xea\x02\"Google::Ads::GoogleAds::V1::Errorsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_RANGEERRORENUM_RANGEERROR = _descriptor.EnumDescriptor(
  name='RangeError',
  full_name='google.ads.googleads.v1.errors.RangeErrorEnum.RangeError',
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
      name='TOO_LOW', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TOO_HIGH', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=138,
  serialized_end=207,
)
_sym_db.RegisterEnumDescriptor(_RANGEERRORENUM_RANGEERROR)


_RANGEERRORENUM = _descriptor.Descriptor(
  name='RangeErrorEnum',
  full_name='google.ads.googleads.v1.errors.RangeErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _RANGEERRORENUM_RANGEERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=120,
  serialized_end=207,
)

_RANGEERRORENUM_RANGEERROR.containing_type = _RANGEERRORENUM
DESCRIPTOR.message_types_by_name['RangeErrorEnum'] = _RANGEERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RangeErrorEnum = _reflection.GeneratedProtocolMessageType('RangeErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _RANGEERRORENUM,
  __module__ = 'google.ads.googleads_v1.proto.errors.range_error_pb2'
  ,
  __doc__ = """Container for enum describing possible range errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.errors.RangeErrorEnum)
  ))
_sym_db.RegisterMessage(RangeErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
