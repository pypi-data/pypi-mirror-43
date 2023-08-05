# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/errors/ad_customizer_error.proto

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
  name='google/ads/googleads_v1/proto/errors/ad_customizer_error.proto',
  package='google.ads.googleads.v1.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v1.errorsB\026AdCustomizerErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v1/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V1.Errors\312\002\036Google\\Ads\\GoogleAds\\V1\\Errors\352\002\"Google::Ads::GoogleAds::V1::Errors'),
  serialized_pb=_b('\n>google/ads/googleads_v1/proto/errors/ad_customizer_error.proto\x12\x1egoogle.ads.googleads.v1.errors\x1a\x1cgoogle/api/annotations.proto\"\xe8\x01\n\x15\x41\x64\x43ustomizerErrorEnum\"\xce\x01\n\x11\x41\x64\x43ustomizerError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12!\n\x1d\x43OUNTDOWN_INVALID_DATE_FORMAT\x10\x02\x12\x1a\n\x16\x43OUNTDOWN_DATE_IN_PAST\x10\x03\x12\x1c\n\x18\x43OUNTDOWN_INVALID_LOCALE\x10\x04\x12\'\n#COUNTDOWN_INVALID_START_DAYS_BEFORE\x10\x05\x12\x15\n\x11UNKNOWN_USER_LIST\x10\x06\x42\xf1\x01\n\"com.google.ads.googleads.v1.errorsB\x16\x41\x64\x43ustomizerErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v1/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V1.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V1\\Errors\xea\x02\"Google::Ads::GoogleAds::V1::Errorsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_ADCUSTOMIZERERRORENUM_ADCUSTOMIZERERROR = _descriptor.EnumDescriptor(
  name='AdCustomizerError',
  full_name='google.ads.googleads.v1.errors.AdCustomizerErrorEnum.AdCustomizerError',
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
      name='COUNTDOWN_INVALID_DATE_FORMAT', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='COUNTDOWN_DATE_IN_PAST', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='COUNTDOWN_INVALID_LOCALE', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='COUNTDOWN_INVALID_START_DAYS_BEFORE', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_USER_LIST', index=6, number=6,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=155,
  serialized_end=361,
)
_sym_db.RegisterEnumDescriptor(_ADCUSTOMIZERERRORENUM_ADCUSTOMIZERERROR)


_ADCUSTOMIZERERRORENUM = _descriptor.Descriptor(
  name='AdCustomizerErrorEnum',
  full_name='google.ads.googleads.v1.errors.AdCustomizerErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ADCUSTOMIZERERRORENUM_ADCUSTOMIZERERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=129,
  serialized_end=361,
)

_ADCUSTOMIZERERRORENUM_ADCUSTOMIZERERROR.containing_type = _ADCUSTOMIZERERRORENUM
DESCRIPTOR.message_types_by_name['AdCustomizerErrorEnum'] = _ADCUSTOMIZERERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AdCustomizerErrorEnum = _reflection.GeneratedProtocolMessageType('AdCustomizerErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _ADCUSTOMIZERERRORENUM,
  __module__ = 'google.ads.googleads_v1.proto.errors.ad_customizer_error_pb2'
  ,
  __doc__ = """Container for enum describing possible ad customizer errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.errors.AdCustomizerErrorEnum)
  ))
_sym_db.RegisterMessage(AdCustomizerErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
