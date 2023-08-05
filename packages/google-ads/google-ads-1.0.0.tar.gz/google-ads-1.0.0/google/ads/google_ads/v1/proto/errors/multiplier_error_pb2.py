# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/errors/multiplier_error.proto

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
  name='google/ads/googleads_v1/proto/errors/multiplier_error.proto',
  package='google.ads.googleads.v1.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v1.errorsB\024MultiplierErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v1/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V1.Errors\312\002\036Google\\Ads\\GoogleAds\\V1\\Errors\352\002\"Google::Ads::GoogleAds::V1::Errors'),
  serialized_pb=_b('\n;google/ads/googleads_v1/proto/errors/multiplier_error.proto\x12\x1egoogle.ads.googleads.v1.errors\x1a\x1cgoogle/api/annotations.proto\"\xcf\x04\n\x13MultiplierErrorEnum\"\xb7\x04\n\x0fMultiplierError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x17\n\x13MULTIPLIER_TOO_HIGH\x10\x02\x12\x16\n\x12MULTIPLIER_TOO_LOW\x10\x03\x12\x1e\n\x1aTOO_MANY_FRACTIONAL_DIGITS\x10\x04\x12/\n+MULTIPLIER_NOT_ALLOWED_FOR_BIDDING_STRATEGY\x10\x05\x12\x33\n/MULTIPLIER_NOT_ALLOWED_WHEN_BASE_BID_IS_MISSING\x10\x06\x12\x1b\n\x17NO_MULTIPLIER_SPECIFIED\x10\x07\x12\x30\n,MULTIPLIER_CAUSES_BID_TO_EXCEED_DAILY_BUDGET\x10\x08\x12\x32\n.MULTIPLIER_CAUSES_BID_TO_EXCEED_MONTHLY_BUDGET\x10\t\x12\x31\n-MULTIPLIER_CAUSES_BID_TO_EXCEED_CUSTOM_BUDGET\x10\n\x12\x33\n/MULTIPLIER_CAUSES_BID_TO_EXCEED_MAX_ALLOWED_BID\x10\x0b\x12\x31\n-BID_LESS_THAN_MIN_ALLOWED_BID_WITH_MULTIPLIER\x10\x0c\x12\x31\n-MULTIPLIER_AND_BIDDING_STRATEGY_TYPE_MISMATCH\x10\rB\xef\x01\n\"com.google.ads.googleads.v1.errorsB\x14MultiplierErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v1/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V1.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V1\\Errors\xea\x02\"Google::Ads::GoogleAds::V1::Errorsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_MULTIPLIERERRORENUM_MULTIPLIERERROR = _descriptor.EnumDescriptor(
  name='MultiplierError',
  full_name='google.ads.googleads.v1.errors.MultiplierErrorEnum.MultiplierError',
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
      name='MULTIPLIER_TOO_HIGH', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MULTIPLIER_TOO_LOW', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TOO_MANY_FRACTIONAL_DIGITS', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MULTIPLIER_NOT_ALLOWED_FOR_BIDDING_STRATEGY', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MULTIPLIER_NOT_ALLOWED_WHEN_BASE_BID_IS_MISSING', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NO_MULTIPLIER_SPECIFIED', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MULTIPLIER_CAUSES_BID_TO_EXCEED_DAILY_BUDGET', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MULTIPLIER_CAUSES_BID_TO_EXCEED_MONTHLY_BUDGET', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MULTIPLIER_CAUSES_BID_TO_EXCEED_CUSTOM_BUDGET', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MULTIPLIER_CAUSES_BID_TO_EXCEED_MAX_ALLOWED_BID', index=11, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BID_LESS_THAN_MIN_ALLOWED_BID_WITH_MULTIPLIER', index=12, number=12,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MULTIPLIER_AND_BIDDING_STRATEGY_TYPE_MISMATCH', index=13, number=13,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=150,
  serialized_end=717,
)
_sym_db.RegisterEnumDescriptor(_MULTIPLIERERRORENUM_MULTIPLIERERROR)


_MULTIPLIERERRORENUM = _descriptor.Descriptor(
  name='MultiplierErrorEnum',
  full_name='google.ads.googleads.v1.errors.MultiplierErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MULTIPLIERERRORENUM_MULTIPLIERERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=126,
  serialized_end=717,
)

_MULTIPLIERERRORENUM_MULTIPLIERERROR.containing_type = _MULTIPLIERERRORENUM
DESCRIPTOR.message_types_by_name['MultiplierErrorEnum'] = _MULTIPLIERERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MultiplierErrorEnum = _reflection.GeneratedProtocolMessageType('MultiplierErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _MULTIPLIERERRORENUM,
  __module__ = 'google.ads.googleads_v1.proto.errors.multiplier_error_pb2'
  ,
  __doc__ = """Container for enum describing possible multiplier errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.errors.MultiplierErrorEnum)
  ))
_sym_db.RegisterMessage(MultiplierErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
