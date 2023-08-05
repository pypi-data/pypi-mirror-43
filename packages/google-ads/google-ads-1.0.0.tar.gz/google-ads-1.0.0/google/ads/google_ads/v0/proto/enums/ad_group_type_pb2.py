# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/enums/ad_group_type.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/enums/ad_group_type.proto',
  package='google.ads.googleads.v0.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v0.enumsB\020AdGroupTypeProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v0/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V0.Enums\312\002\035Google\\Ads\\GoogleAds\\V0\\Enums\352\002!Google::Ads::GoogleAds::V0::Enums'),
  serialized_pb=_b('\n7google/ads/googleads_v0/proto/enums/ad_group_type.proto\x12\x1dgoogle.ads.googleads.v0.enums\"\xb4\x02\n\x0f\x41\x64GroupTypeEnum\"\xa0\x02\n\x0b\x41\x64GroupType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x13\n\x0fSEARCH_STANDARD\x10\x02\x12\x14\n\x10\x44ISPLAY_STANDARD\x10\x03\x12\x18\n\x14SHOPPING_PRODUCT_ADS\x10\x04\x12\r\n\tHOTEL_ADS\x10\x06\x12\x16\n\x12SHOPPING_SMART_ADS\x10\x07\x12\x10\n\x0cVIDEO_BUMPER\x10\x08\x12\x1d\n\x19VIDEO_TRUE_VIEW_IN_STREAM\x10\t\x12\x1e\n\x1aVIDEO_TRUE_VIEW_IN_DISPLAY\x10\n\x12!\n\x1dVIDEO_NON_SKIPPABLE_IN_STREAM\x10\x0b\x12\x13\n\x0fVIDEO_OUTSTREAM\x10\x0c\x42\xe5\x01\n!com.google.ads.googleads.v0.enumsB\x10\x41\x64GroupTypeProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v0/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V0.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V0\\Enums\xea\x02!Google::Ads::GoogleAds::V0::Enumsb\x06proto3')
)



_ADGROUPTYPEENUM_ADGROUPTYPE = _descriptor.EnumDescriptor(
  name='AdGroupType',
  full_name='google.ads.googleads.v0.enums.AdGroupTypeEnum.AdGroupType',
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
      name='SEARCH_STANDARD', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DISPLAY_STANDARD', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SHOPPING_PRODUCT_ADS', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HOTEL_ADS', index=5, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SHOPPING_SMART_ADS', index=6, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_BUMPER', index=7, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_TRUE_VIEW_IN_STREAM', index=8, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_TRUE_VIEW_IN_DISPLAY', index=9, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_NON_SKIPPABLE_IN_STREAM', index=10, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_OUTSTREAM', index=11, number=12,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=111,
  serialized_end=399,
)
_sym_db.RegisterEnumDescriptor(_ADGROUPTYPEENUM_ADGROUPTYPE)


_ADGROUPTYPEENUM = _descriptor.Descriptor(
  name='AdGroupTypeEnum',
  full_name='google.ads.googleads.v0.enums.AdGroupTypeEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ADGROUPTYPEENUM_ADGROUPTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=91,
  serialized_end=399,
)

_ADGROUPTYPEENUM_ADGROUPTYPE.containing_type = _ADGROUPTYPEENUM
DESCRIPTOR.message_types_by_name['AdGroupTypeEnum'] = _ADGROUPTYPEENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AdGroupTypeEnum = _reflection.GeneratedProtocolMessageType('AdGroupTypeEnum', (_message.Message,), dict(
  DESCRIPTOR = _ADGROUPTYPEENUM,
  __module__ = 'google.ads.googleads_v0.proto.enums.ad_group_type_pb2'
  ,
  __doc__ = """Defines types of an ad group, specific to a particular campaign channel
  type. This type drives validations that restrict which entities can be
  added to the ad group.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.enums.AdGroupTypeEnum)
  ))
_sym_db.RegisterMessage(AdGroupTypeEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
