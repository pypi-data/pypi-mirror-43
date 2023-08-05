# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/enums/ad_group_criterion_status.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/enums/ad_group_criterion_status.proto',
  package='google.ads.googleads.v0.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v0.enumsB\033AdGroupCriterionStatusProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v0/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V0.Enums\312\002\035Google\\Ads\\GoogleAds\\V0\\Enums\352\002!Google::Ads::GoogleAds::V0::Enums'),
  serialized_pb=_b('\nCgoogle/ads/googleads_v0/proto/enums/ad_group_criterion_status.proto\x12\x1dgoogle.ads.googleads.v0.enums\"z\n\x1a\x41\x64GroupCriterionStatusEnum\"\\\n\x16\x41\x64GroupCriterionStatus\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0b\n\x07\x45NABLED\x10\x02\x12\n\n\x06PAUSED\x10\x03\x12\x0b\n\x07REMOVED\x10\x04\x42\xf0\x01\n!com.google.ads.googleads.v0.enumsB\x1b\x41\x64GroupCriterionStatusProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v0/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V0.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V0\\Enums\xea\x02!Google::Ads::GoogleAds::V0::Enumsb\x06proto3')
)



_ADGROUPCRITERIONSTATUSENUM_ADGROUPCRITERIONSTATUS = _descriptor.EnumDescriptor(
  name='AdGroupCriterionStatus',
  full_name='google.ads.googleads.v0.enums.AdGroupCriterionStatusEnum.AdGroupCriterionStatus',
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
      name='ENABLED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PAUSED', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REMOVED', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=132,
  serialized_end=224,
)
_sym_db.RegisterEnumDescriptor(_ADGROUPCRITERIONSTATUSENUM_ADGROUPCRITERIONSTATUS)


_ADGROUPCRITERIONSTATUSENUM = _descriptor.Descriptor(
  name='AdGroupCriterionStatusEnum',
  full_name='google.ads.googleads.v0.enums.AdGroupCriterionStatusEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ADGROUPCRITERIONSTATUSENUM_ADGROUPCRITERIONSTATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=102,
  serialized_end=224,
)

_ADGROUPCRITERIONSTATUSENUM_ADGROUPCRITERIONSTATUS.containing_type = _ADGROUPCRITERIONSTATUSENUM
DESCRIPTOR.message_types_by_name['AdGroupCriterionStatusEnum'] = _ADGROUPCRITERIONSTATUSENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AdGroupCriterionStatusEnum = _reflection.GeneratedProtocolMessageType('AdGroupCriterionStatusEnum', (_message.Message,), dict(
  DESCRIPTOR = _ADGROUPCRITERIONSTATUSENUM,
  __module__ = 'google.ads.googleads_v0.proto.enums.ad_group_criterion_status_pb2'
  ,
  __doc__ = """Message describing AdGroupCriterion statuses.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.enums.AdGroupCriterionStatusEnum)
  ))
_sym_db.RegisterMessage(AdGroupCriterionStatusEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
