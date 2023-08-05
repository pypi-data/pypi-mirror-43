# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/enums/ad_group_ad_rotation_mode.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/enums/ad_group_ad_rotation_mode.proto',
  package='google.ads.googleads.v0.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v0.enumsB\032AdGroupAdRotationModeProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v0/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V0.Enums\312\002\035Google\\Ads\\GoogleAds\\V0\\Enums\352\002!Google::Ads::GoogleAds::V0::Enums'),
  serialized_pb=_b('\nCgoogle/ads/googleads_v0/proto/enums/ad_group_ad_rotation_mode.proto\x12\x1dgoogle.ads.googleads.v0.enums\"t\n\x19\x41\x64GroupAdRotationModeEnum\"W\n\x15\x41\x64GroupAdRotationMode\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0c\n\x08OPTIMIZE\x10\x02\x12\x12\n\x0eROTATE_FOREVER\x10\x03\x42\xef\x01\n!com.google.ads.googleads.v0.enumsB\x1a\x41\x64GroupAdRotationModeProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v0/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V0.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V0\\Enums\xea\x02!Google::Ads::GoogleAds::V0::Enumsb\x06proto3')
)



_ADGROUPADROTATIONMODEENUM_ADGROUPADROTATIONMODE = _descriptor.EnumDescriptor(
  name='AdGroupAdRotationMode',
  full_name='google.ads.googleads.v0.enums.AdGroupAdRotationModeEnum.AdGroupAdRotationMode',
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
      name='OPTIMIZE', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ROTATE_FOREVER', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=131,
  serialized_end=218,
)
_sym_db.RegisterEnumDescriptor(_ADGROUPADROTATIONMODEENUM_ADGROUPADROTATIONMODE)


_ADGROUPADROTATIONMODEENUM = _descriptor.Descriptor(
  name='AdGroupAdRotationModeEnum',
  full_name='google.ads.googleads.v0.enums.AdGroupAdRotationModeEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ADGROUPADROTATIONMODEENUM_ADGROUPADROTATIONMODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=102,
  serialized_end=218,
)

_ADGROUPADROTATIONMODEENUM_ADGROUPADROTATIONMODE.containing_type = _ADGROUPADROTATIONMODEENUM
DESCRIPTOR.message_types_by_name['AdGroupAdRotationModeEnum'] = _ADGROUPADROTATIONMODEENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AdGroupAdRotationModeEnum = _reflection.GeneratedProtocolMessageType('AdGroupAdRotationModeEnum', (_message.Message,), dict(
  DESCRIPTOR = _ADGROUPADROTATIONMODEENUM,
  __module__ = 'google.ads.googleads_v0.proto.enums.ad_group_ad_rotation_mode_pb2'
  ,
  __doc__ = """Container for enum describing possible ad rotation modes of ads within
  an ad group.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.enums.AdGroupAdRotationModeEnum)
  ))
_sym_db.RegisterMessage(AdGroupAdRotationModeEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
