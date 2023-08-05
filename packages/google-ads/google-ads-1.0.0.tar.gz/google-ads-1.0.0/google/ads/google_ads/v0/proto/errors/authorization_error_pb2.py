# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/errors/authorization_error.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/errors/authorization_error.proto',
  package='google.ads.googleads.v0.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v0.errorsB\027AuthorizationErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v0/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V0.Errors\312\002\036Google\\Ads\\GoogleAds\\V0\\Errors\352\002\"Google::Ads::GoogleAds::V0::Errors'),
  serialized_pb=_b('\n>google/ads/googleads_v0/proto/errors/authorization_error.proto\x12\x1egoogle.ads.googleads.v0.errors\"\x8e\x02\n\x16\x41uthorizationErrorEnum\"\xf3\x01\n\x12\x41uthorizationError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x1a\n\x16USER_PERMISSION_DENIED\x10\x02\x12#\n\x1f\x44\x45VELOPER_TOKEN_NOT_WHITELISTED\x10\x03\x12\x1e\n\x1a\x44\x45VELOPER_TOKEN_PROHIBITED\x10\x04\x12\x14\n\x10PROJECT_DISABLED\x10\x05\x12\x17\n\x13\x41UTHORIZATION_ERROR\x10\x06\x12\x18\n\x14\x41\x43TION_NOT_PERMITTED\x10\x07\x12\x15\n\x11INCOMPLETE_SIGNUP\x10\x08\x42\xf2\x01\n\"com.google.ads.googleads.v0.errorsB\x17\x41uthorizationErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v0/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V0.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V0\\Errors\xea\x02\"Google::Ads::GoogleAds::V0::Errorsb\x06proto3')
)



_AUTHORIZATIONERRORENUM_AUTHORIZATIONERROR = _descriptor.EnumDescriptor(
  name='AuthorizationError',
  full_name='google.ads.googleads.v0.errors.AuthorizationErrorEnum.AuthorizationError',
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
      name='USER_PERMISSION_DENIED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEVELOPER_TOKEN_NOT_WHITELISTED', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEVELOPER_TOKEN_PROHIBITED', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PROJECT_DISABLED', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AUTHORIZATION_ERROR', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ACTION_NOT_PERMITTED', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INCOMPLETE_SIGNUP', index=8, number=8,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=126,
  serialized_end=369,
)
_sym_db.RegisterEnumDescriptor(_AUTHORIZATIONERRORENUM_AUTHORIZATIONERROR)


_AUTHORIZATIONERRORENUM = _descriptor.Descriptor(
  name='AuthorizationErrorEnum',
  full_name='google.ads.googleads.v0.errors.AuthorizationErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _AUTHORIZATIONERRORENUM_AUTHORIZATIONERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=99,
  serialized_end=369,
)

_AUTHORIZATIONERRORENUM_AUTHORIZATIONERROR.containing_type = _AUTHORIZATIONERRORENUM
DESCRIPTOR.message_types_by_name['AuthorizationErrorEnum'] = _AUTHORIZATIONERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AuthorizationErrorEnum = _reflection.GeneratedProtocolMessageType('AuthorizationErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _AUTHORIZATIONERRORENUM,
  __module__ = 'google.ads.googleads_v0.proto.errors.authorization_error_pb2'
  ,
  __doc__ = """Container for enum describing possible authorization errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.errors.AuthorizationErrorEnum)
  ))
_sym_db.RegisterMessage(AuthorizationErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
