# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/errors/media_file_error.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/errors/media_file_error.proto',
  package='google.ads.googleads.v0.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v0.errorsB\023MediaFileErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v0/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V0.Errors\312\002\036Google\\Ads\\GoogleAds\\V0\\Errors\352\002\"Google::Ads::GoogleAds::V0::Errors'),
  serialized_pb=_b('\n;google/ads/googleads_v0/proto/errors/media_file_error.proto\x12\x1egoogle.ads.googleads.v0.errors\"\x97\x06\n\x12MediaFileErrorEnum\"\x80\x06\n\x0eMediaFileError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x1f\n\x1b\x43\x41NNOT_CREATE_STANDARD_ICON\x10\x02\x12\x30\n,CANNOT_SELECT_STANDARD_ICON_WITH_OTHER_TYPES\x10\x03\x12)\n%CANNOT_SPECIFY_MEDIA_FILE_ID_AND_DATA\x10\x04\x12\x13\n\x0f\x44UPLICATE_MEDIA\x10\x05\x12\x0f\n\x0b\x45MPTY_FIELD\x10\x06\x12\'\n#RESOURCE_REFERENCED_IN_MULTIPLE_OPS\x10\x07\x12*\n&FIELD_NOT_SUPPORTED_FOR_MEDIA_SUB_TYPE\x10\x08\x12\x19\n\x15INVALID_MEDIA_FILE_ID\x10\t\x12\x1a\n\x16INVALID_MEDIA_SUB_TYPE\x10\n\x12\x1b\n\x17INVALID_MEDIA_FILE_TYPE\x10\x0b\x12\x15\n\x11INVALID_MIME_TYPE\x10\x0c\x12\x18\n\x14INVALID_REFERENCE_ID\x10\r\x12\x17\n\x13INVALID_YOU_TUBE_ID\x10\x0e\x12!\n\x1dMEDIA_FILE_FAILED_TRANSCODING\x10\x0f\x12\x18\n\x14MEDIA_NOT_TRANSCODED\x10\x10\x12-\n)MEDIA_TYPE_DOES_NOT_MATCH_MEDIA_FILE_TYPE\x10\x11\x12\x17\n\x13NO_FIELDS_SPECIFIED\x10\x12\x12\"\n\x1eNULL_REFERENCE_ID_AND_MEDIA_ID\x10\x13\x12\x0c\n\x08TOO_LONG\x10\x14\x12\x14\n\x10UNSUPPORTED_TYPE\x10\x15\x12 \n\x1cYOU_TUBE_SERVICE_UNAVAILABLE\x10\x16\x12,\n(YOU_TUBE_VIDEO_HAS_NON_POSITIVE_DURATION\x10\x17\x12\x1c\n\x18YOU_TUBE_VIDEO_NOT_FOUND\x10\x18\x42\xee\x01\n\"com.google.ads.googleads.v0.errorsB\x13MediaFileErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v0/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V0.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V0\\Errors\xea\x02\"Google::Ads::GoogleAds::V0::Errorsb\x06proto3')
)



_MEDIAFILEERRORENUM_MEDIAFILEERROR = _descriptor.EnumDescriptor(
  name='MediaFileError',
  full_name='google.ads.googleads.v0.errors.MediaFileErrorEnum.MediaFileError',
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
      name='CANNOT_CREATE_STANDARD_ICON', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_SELECT_STANDARD_ICON_WITH_OTHER_TYPES', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_SPECIFY_MEDIA_FILE_ID_AND_DATA', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DUPLICATE_MEDIA', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EMPTY_FIELD', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RESOURCE_REFERENCED_IN_MULTIPLE_OPS', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FIELD_NOT_SUPPORTED_FOR_MEDIA_SUB_TYPE', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_MEDIA_FILE_ID', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_MEDIA_SUB_TYPE', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_MEDIA_FILE_TYPE', index=11, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_MIME_TYPE', index=12, number=12,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_REFERENCE_ID', index=13, number=13,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_YOU_TUBE_ID', index=14, number=14,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MEDIA_FILE_FAILED_TRANSCODING', index=15, number=15,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MEDIA_NOT_TRANSCODED', index=16, number=16,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MEDIA_TYPE_DOES_NOT_MATCH_MEDIA_FILE_TYPE', index=17, number=17,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NO_FIELDS_SPECIFIED', index=18, number=18,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NULL_REFERENCE_ID_AND_MEDIA_ID', index=19, number=19,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TOO_LONG', index=20, number=20,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNSUPPORTED_TYPE', index=21, number=21,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='YOU_TUBE_SERVICE_UNAVAILABLE', index=22, number=22,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='YOU_TUBE_VIDEO_HAS_NON_POSITIVE_DURATION', index=23, number=23,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='YOU_TUBE_VIDEO_NOT_FOUND', index=24, number=24,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=119,
  serialized_end=887,
)
_sym_db.RegisterEnumDescriptor(_MEDIAFILEERRORENUM_MEDIAFILEERROR)


_MEDIAFILEERRORENUM = _descriptor.Descriptor(
  name='MediaFileErrorEnum',
  full_name='google.ads.googleads.v0.errors.MediaFileErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MEDIAFILEERRORENUM_MEDIAFILEERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=96,
  serialized_end=887,
)

_MEDIAFILEERRORENUM_MEDIAFILEERROR.containing_type = _MEDIAFILEERRORENUM
DESCRIPTOR.message_types_by_name['MediaFileErrorEnum'] = _MEDIAFILEERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MediaFileErrorEnum = _reflection.GeneratedProtocolMessageType('MediaFileErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _MEDIAFILEERRORENUM,
  __module__ = 'google.ads.googleads_v0.proto.errors.media_file_error_pb2'
  ,
  __doc__ = """Container for enum describing possible media file errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.errors.MediaFileErrorEnum)
  ))
_sym_db.RegisterMessage(MediaFileErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
