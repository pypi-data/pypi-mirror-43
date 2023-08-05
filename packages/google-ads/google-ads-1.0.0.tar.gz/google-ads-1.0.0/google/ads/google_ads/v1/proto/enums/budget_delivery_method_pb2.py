# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/enums/budget_delivery_method.proto

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
  name='google/ads/googleads_v1/proto/enums/budget_delivery_method.proto',
  package='google.ads.googleads.v1.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v1.enumsB\031BudgetDeliveryMethodProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v1/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V1.Enums\312\002\035Google\\Ads\\GoogleAds\\V1\\Enums\352\002!Google::Ads::GoogleAds::V1::Enums'),
  serialized_pb=_b('\n@google/ads/googleads_v1/proto/enums/budget_delivery_method.proto\x12\x1dgoogle.ads.googleads.v1.enums\x1a\x1cgoogle/api/annotations.proto\"o\n\x18\x42udgetDeliveryMethodEnum\"S\n\x14\x42udgetDeliveryMethod\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0c\n\x08STANDARD\x10\x02\x12\x0f\n\x0b\x41\x43\x43\x45LERATED\x10\x03\x42\xee\x01\n!com.google.ads.googleads.v1.enumsB\x19\x42udgetDeliveryMethodProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v1/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V1.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V1\\Enums\xea\x02!Google::Ads::GoogleAds::V1::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_BUDGETDELIVERYMETHODENUM_BUDGETDELIVERYMETHOD = _descriptor.EnumDescriptor(
  name='BudgetDeliveryMethod',
  full_name='google.ads.googleads.v1.enums.BudgetDeliveryMethodEnum.BudgetDeliveryMethod',
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
      name='STANDARD', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ACCELERATED', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=157,
  serialized_end=240,
)
_sym_db.RegisterEnumDescriptor(_BUDGETDELIVERYMETHODENUM_BUDGETDELIVERYMETHOD)


_BUDGETDELIVERYMETHODENUM = _descriptor.Descriptor(
  name='BudgetDeliveryMethodEnum',
  full_name='google.ads.googleads.v1.enums.BudgetDeliveryMethodEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _BUDGETDELIVERYMETHODENUM_BUDGETDELIVERYMETHOD,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=129,
  serialized_end=240,
)

_BUDGETDELIVERYMETHODENUM_BUDGETDELIVERYMETHOD.containing_type = _BUDGETDELIVERYMETHODENUM
DESCRIPTOR.message_types_by_name['BudgetDeliveryMethodEnum'] = _BUDGETDELIVERYMETHODENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BudgetDeliveryMethodEnum = _reflection.GeneratedProtocolMessageType('BudgetDeliveryMethodEnum', (_message.Message,), dict(
  DESCRIPTOR = _BUDGETDELIVERYMETHODENUM,
  __module__ = 'google.ads.googleads_v1.proto.enums.budget_delivery_method_pb2'
  ,
  __doc__ = """Message describing Budget delivery methods. A delivery method determines
  the rate at which the Budget is spent.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.enums.BudgetDeliveryMethodEnum)
  ))
_sym_db.RegisterMessage(BudgetDeliveryMethodEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
