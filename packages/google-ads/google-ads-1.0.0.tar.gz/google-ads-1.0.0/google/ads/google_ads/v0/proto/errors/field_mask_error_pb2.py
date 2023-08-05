# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/errors/field_mask_error.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/errors/field_mask_error.proto',
  package='google.ads.googleads.v0.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v0.errorsB\023FieldMaskErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v0/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V0.Errors\312\002\036Google\\Ads\\GoogleAds\\V0\\Errors\352\002\"Google::Ads::GoogleAds::V0::Errors'),
  serialized_pb=_b('\n;google/ads/googleads_v0/proto/errors/field_mask_error.proto\x12\x1egoogle.ads.googleads.v0.errors\"\xa7\x01\n\x12\x46ieldMaskErrorEnum\"\x90\x01\n\x0e\x46ieldMaskError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x16\n\x12\x46IELD_MASK_MISSING\x10\x05\x12\x1a\n\x16\x46IELD_MASK_NOT_ALLOWED\x10\x04\x12\x13\n\x0f\x46IELD_NOT_FOUND\x10\x02\x12\x17\n\x13\x46IELD_HAS_SUBFIELDS\x10\x03\x42\xee\x01\n\"com.google.ads.googleads.v0.errorsB\x13\x46ieldMaskErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v0/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V0.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V0\\Errors\xea\x02\"Google::Ads::GoogleAds::V0::Errorsb\x06proto3')
)



_FIELDMASKERRORENUM_FIELDMASKERROR = _descriptor.EnumDescriptor(
  name='FieldMaskError',
  full_name='google.ads.googleads.v0.errors.FieldMaskErrorEnum.FieldMaskError',
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
      name='FIELD_MASK_MISSING', index=2, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FIELD_MASK_NOT_ALLOWED', index=3, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FIELD_NOT_FOUND', index=4, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FIELD_HAS_SUBFIELDS', index=5, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=119,
  serialized_end=263,
)
_sym_db.RegisterEnumDescriptor(_FIELDMASKERRORENUM_FIELDMASKERROR)


_FIELDMASKERRORENUM = _descriptor.Descriptor(
  name='FieldMaskErrorEnum',
  full_name='google.ads.googleads.v0.errors.FieldMaskErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _FIELDMASKERRORENUM_FIELDMASKERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=96,
  serialized_end=263,
)

_FIELDMASKERRORENUM_FIELDMASKERROR.containing_type = _FIELDMASKERRORENUM
DESCRIPTOR.message_types_by_name['FieldMaskErrorEnum'] = _FIELDMASKERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FieldMaskErrorEnum = _reflection.GeneratedProtocolMessageType('FieldMaskErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _FIELDMASKERRORENUM,
  __module__ = 'google.ads.googleads_v0.proto.errors.field_mask_error_pb2'
  ,
  __doc__ = """Container for enum describing possible field mask errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.errors.FieldMaskErrorEnum)
  ))
_sym_db.RegisterMessage(FieldMaskErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
