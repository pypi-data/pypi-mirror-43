# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/errors/authentication_error.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/errors/authentication_error.proto',
  package='google.ads.googleads.v0.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v0.errorsB\030AuthenticationErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v0/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V0.Errors\312\002\036Google\\Ads\\GoogleAds\\V0\\Errors\352\002\"Google::Ads::GoogleAds::V0::Errors'),
  serialized_pb=_b('\n?google/ads/googleads_v0/proto/errors/authentication_error.proto\x12\x1egoogle.ads.googleads.v0.errors\"\xe8\x04\n\x17\x41uthenticationErrorEnum\"\xcc\x04\n\x13\x41uthenticationError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x18\n\x14\x41UTHENTICATION_ERROR\x10\x02\x12\x1e\n\x1a\x43LIENT_CUSTOMER_ID_INVALID\x10\x05\x12\x16\n\x12\x43USTOMER_NOT_FOUND\x10\x08\x12\x1a\n\x16GOOGLE_ACCOUNT_DELETED\x10\t\x12!\n\x1dGOOGLE_ACCOUNT_COOKIE_INVALID\x10\n\x12(\n$GOOGLE_ACCOUNT_AUTHENTICATION_FAILED\x10\x19\x12-\n)GOOGLE_ACCOUNT_USER_AND_ADS_USER_MISMATCH\x10\x0c\x12\x19\n\x15LOGIN_COOKIE_REQUIRED\x10\r\x12\x10\n\x0cNOT_ADS_USER\x10\x0e\x12\x17\n\x13OAUTH_TOKEN_INVALID\x10\x0f\x12\x17\n\x13OAUTH_TOKEN_EXPIRED\x10\x10\x12\x18\n\x14OAUTH_TOKEN_DISABLED\x10\x11\x12\x17\n\x13OAUTH_TOKEN_REVOKED\x10\x12\x12\x1e\n\x1aOAUTH_TOKEN_HEADER_INVALID\x10\x13\x12\x18\n\x14LOGIN_COOKIE_INVALID\x10\x14\x12\x13\n\x0fUSER_ID_INVALID\x10\x16\x12&\n\"TWO_STEP_VERIFICATION_NOT_ENROLLED\x10\x17\x12$\n ADVANCED_PROTECTION_NOT_ENROLLED\x10\x18\x42\xf3\x01\n\"com.google.ads.googleads.v0.errorsB\x18\x41uthenticationErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v0/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V0.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V0\\Errors\xea\x02\"Google::Ads::GoogleAds::V0::Errorsb\x06proto3')
)



_AUTHENTICATIONERRORENUM_AUTHENTICATIONERROR = _descriptor.EnumDescriptor(
  name='AuthenticationError',
  full_name='google.ads.googleads.v0.errors.AuthenticationErrorEnum.AuthenticationError',
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
      name='AUTHENTICATION_ERROR', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CLIENT_CUSTOMER_ID_INVALID', index=3, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CUSTOMER_NOT_FOUND', index=4, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GOOGLE_ACCOUNT_DELETED', index=5, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GOOGLE_ACCOUNT_COOKIE_INVALID', index=6, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GOOGLE_ACCOUNT_AUTHENTICATION_FAILED', index=7, number=25,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GOOGLE_ACCOUNT_USER_AND_ADS_USER_MISMATCH', index=8, number=12,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LOGIN_COOKIE_REQUIRED', index=9, number=13,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NOT_ADS_USER', index=10, number=14,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OAUTH_TOKEN_INVALID', index=11, number=15,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OAUTH_TOKEN_EXPIRED', index=12, number=16,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OAUTH_TOKEN_DISABLED', index=13, number=17,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OAUTH_TOKEN_REVOKED', index=14, number=18,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OAUTH_TOKEN_HEADER_INVALID', index=15, number=19,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LOGIN_COOKIE_INVALID', index=16, number=20,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='USER_ID_INVALID', index=17, number=22,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TWO_STEP_VERIFICATION_NOT_ENROLLED', index=18, number=23,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ADVANCED_PROTECTION_NOT_ENROLLED', index=19, number=24,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=128,
  serialized_end=716,
)
_sym_db.RegisterEnumDescriptor(_AUTHENTICATIONERRORENUM_AUTHENTICATIONERROR)


_AUTHENTICATIONERRORENUM = _descriptor.Descriptor(
  name='AuthenticationErrorEnum',
  full_name='google.ads.googleads.v0.errors.AuthenticationErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _AUTHENTICATIONERRORENUM_AUTHENTICATIONERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=100,
  serialized_end=716,
)

_AUTHENTICATIONERRORENUM_AUTHENTICATIONERROR.containing_type = _AUTHENTICATIONERRORENUM
DESCRIPTOR.message_types_by_name['AuthenticationErrorEnum'] = _AUTHENTICATIONERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AuthenticationErrorEnum = _reflection.GeneratedProtocolMessageType('AuthenticationErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _AUTHENTICATIONERRORENUM,
  __module__ = 'google.ads.googleads_v0.proto.errors.authentication_error_pb2'
  ,
  __doc__ = """Container for enum describing possible authentication errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.errors.AuthenticationErrorEnum)
  ))
_sym_db.RegisterMessage(AuthenticationErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
