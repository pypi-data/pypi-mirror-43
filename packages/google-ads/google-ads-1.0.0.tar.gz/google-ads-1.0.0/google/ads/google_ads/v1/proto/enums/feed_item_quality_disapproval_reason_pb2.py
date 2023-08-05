# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/enums/feed_item_quality_disapproval_reason.proto

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
  name='google/ads/googleads_v1/proto/enums/feed_item_quality_disapproval_reason.proto',
  package='google.ads.googleads.v1.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v1.enumsB%FeedItemQualityDisapprovalReasonProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v1/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V1.Enums\312\002\035Google\\Ads\\GoogleAds\\V1\\Enums\352\002!Google::Ads::GoogleAds::V1::Enums'),
  serialized_pb=_b('\nNgoogle/ads/googleads_v1/proto/enums/feed_item_quality_disapproval_reason.proto\x12\x1dgoogle.ads.googleads.v1.enums\x1a\x1cgoogle/api/annotations.proto\"\xe0\x06\n$FeedItemQualityDisapprovalReasonEnum\"\xb7\x06\n FeedItemQualityDisapprovalReason\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\"\n\x1ePRICE_TABLE_REPETITIVE_HEADERS\x10\x02\x12&\n\"PRICE_TABLE_REPETITIVE_DESCRIPTION\x10\x03\x12!\n\x1dPRICE_TABLE_INCONSISTENT_ROWS\x10\x04\x12*\n&PRICE_DESCRIPTION_HAS_PRICE_QUALIFIERS\x10\x05\x12\x1e\n\x1aPRICE_UNSUPPORTED_LANGUAGE\x10\x06\x12.\n*PRICE_TABLE_ROW_HEADER_TABLE_TYPE_MISMATCH\x10\x07\x12/\n+PRICE_TABLE_ROW_HEADER_HAS_PROMOTIONAL_TEXT\x10\x08\x12,\n(PRICE_TABLE_ROW_DESCRIPTION_NOT_RELEVANT\x10\t\x12\x34\n0PRICE_TABLE_ROW_DESCRIPTION_HAS_PROMOTIONAL_TEXT\x10\n\x12\x31\n-PRICE_TABLE_ROW_HEADER_DESCRIPTION_REPETITIVE\x10\x0b\x12\x1e\n\x1aPRICE_TABLE_ROW_UNRATEABLE\x10\x0c\x12!\n\x1dPRICE_TABLE_ROW_PRICE_INVALID\x10\r\x12\x1f\n\x1bPRICE_TABLE_ROW_URL_INVALID\x10\x0e\x12)\n%PRICE_HEADER_OR_DESCRIPTION_HAS_PRICE\x10\x0f\x12.\n*STRUCTURED_SNIPPETS_HEADER_POLICY_VIOLATED\x10\x10\x12\'\n#STRUCTURED_SNIPPETS_REPEATED_VALUES\x10\x11\x12,\n(STRUCTURED_SNIPPETS_EDITORIAL_GUIDELINES\x10\x12\x12,\n(STRUCTURED_SNIPPETS_HAS_PROMOTIONAL_TEXT\x10\x13\x42\xfa\x01\n!com.google.ads.googleads.v1.enumsB%FeedItemQualityDisapprovalReasonProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v1/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V1.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V1\\Enums\xea\x02!Google::Ads::GoogleAds::V1::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_FEEDITEMQUALITYDISAPPROVALREASONENUM_FEEDITEMQUALITYDISAPPROVALREASON = _descriptor.EnumDescriptor(
  name='FeedItemQualityDisapprovalReason',
  full_name='google.ads.googleads.v1.enums.FeedItemQualityDisapprovalReasonEnum.FeedItemQualityDisapprovalReason',
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
      name='PRICE_TABLE_REPETITIVE_HEADERS', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRICE_TABLE_REPETITIVE_DESCRIPTION', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRICE_TABLE_INCONSISTENT_ROWS', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRICE_DESCRIPTION_HAS_PRICE_QUALIFIERS', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRICE_UNSUPPORTED_LANGUAGE', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRICE_TABLE_ROW_HEADER_TABLE_TYPE_MISMATCH', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRICE_TABLE_ROW_HEADER_HAS_PROMOTIONAL_TEXT', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRICE_TABLE_ROW_DESCRIPTION_NOT_RELEVANT', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRICE_TABLE_ROW_DESCRIPTION_HAS_PROMOTIONAL_TEXT', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRICE_TABLE_ROW_HEADER_DESCRIPTION_REPETITIVE', index=11, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRICE_TABLE_ROW_UNRATEABLE', index=12, number=12,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRICE_TABLE_ROW_PRICE_INVALID', index=13, number=13,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRICE_TABLE_ROW_URL_INVALID', index=14, number=14,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRICE_HEADER_OR_DESCRIPTION_HAS_PRICE', index=15, number=15,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STRUCTURED_SNIPPETS_HEADER_POLICY_VIOLATED', index=16, number=16,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STRUCTURED_SNIPPETS_REPEATED_VALUES', index=17, number=17,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STRUCTURED_SNIPPETS_EDITORIAL_GUIDELINES', index=18, number=18,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STRUCTURED_SNIPPETS_HAS_PROMOTIONAL_TEXT', index=19, number=19,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=185,
  serialized_end=1008,
)
_sym_db.RegisterEnumDescriptor(_FEEDITEMQUALITYDISAPPROVALREASONENUM_FEEDITEMQUALITYDISAPPROVALREASON)


_FEEDITEMQUALITYDISAPPROVALREASONENUM = _descriptor.Descriptor(
  name='FeedItemQualityDisapprovalReasonEnum',
  full_name='google.ads.googleads.v1.enums.FeedItemQualityDisapprovalReasonEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _FEEDITEMQUALITYDISAPPROVALREASONENUM_FEEDITEMQUALITYDISAPPROVALREASON,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=144,
  serialized_end=1008,
)

_FEEDITEMQUALITYDISAPPROVALREASONENUM_FEEDITEMQUALITYDISAPPROVALREASON.containing_type = _FEEDITEMQUALITYDISAPPROVALREASONENUM
DESCRIPTOR.message_types_by_name['FeedItemQualityDisapprovalReasonEnum'] = _FEEDITEMQUALITYDISAPPROVALREASONENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FeedItemQualityDisapprovalReasonEnum = _reflection.GeneratedProtocolMessageType('FeedItemQualityDisapprovalReasonEnum', (_message.Message,), dict(
  DESCRIPTOR = _FEEDITEMQUALITYDISAPPROVALREASONENUM,
  __module__ = 'google.ads.googleads_v1.proto.enums.feed_item_quality_disapproval_reason_pb2'
  ,
  __doc__ = """Container for enum describing possible quality evaluation disapproval
  reasons of a feed item.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.enums.FeedItemQualityDisapprovalReasonEnum)
  ))
_sym_db.RegisterMessage(FeedItemQualityDisapprovalReasonEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
