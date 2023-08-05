# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/enums/user_list_logical_rule_operator.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/enums/user_list_logical_rule_operator.proto',
  package='google.ads.googleads.v0.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v0.enumsB UserListLogicalRuleOperatorProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v0/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V0.Enums\312\002\035Google\\Ads\\GoogleAds\\V0\\Enums\352\002!Google::Ads::GoogleAds::V0::Enums'),
  serialized_pb=_b('\nIgoogle/ads/googleads_v0/proto/enums/user_list_logical_rule_operator.proto\x12\x1dgoogle.ads.googleads.v0.enums\"z\n\x1fUserListLogicalRuleOperatorEnum\"W\n\x1bUserListLogicalRuleOperator\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x07\n\x03\x41LL\x10\x02\x12\x07\n\x03\x41NY\x10\x03\x12\x08\n\x04NONE\x10\x04\x42\xf5\x01\n!com.google.ads.googleads.v0.enumsB UserListLogicalRuleOperatorProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v0/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V0.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V0\\Enums\xea\x02!Google::Ads::GoogleAds::V0::Enumsb\x06proto3')
)



_USERLISTLOGICALRULEOPERATORENUM_USERLISTLOGICALRULEOPERATOR = _descriptor.EnumDescriptor(
  name='UserListLogicalRuleOperator',
  full_name='google.ads.googleads.v0.enums.UserListLogicalRuleOperatorEnum.UserListLogicalRuleOperator',
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
      name='ALL', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ANY', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NONE', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=143,
  serialized_end=230,
)
_sym_db.RegisterEnumDescriptor(_USERLISTLOGICALRULEOPERATORENUM_USERLISTLOGICALRULEOPERATOR)


_USERLISTLOGICALRULEOPERATORENUM = _descriptor.Descriptor(
  name='UserListLogicalRuleOperatorEnum',
  full_name='google.ads.googleads.v0.enums.UserListLogicalRuleOperatorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _USERLISTLOGICALRULEOPERATORENUM_USERLISTLOGICALRULEOPERATOR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=108,
  serialized_end=230,
)

_USERLISTLOGICALRULEOPERATORENUM_USERLISTLOGICALRULEOPERATOR.containing_type = _USERLISTLOGICALRULEOPERATORENUM
DESCRIPTOR.message_types_by_name['UserListLogicalRuleOperatorEnum'] = _USERLISTLOGICALRULEOPERATORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UserListLogicalRuleOperatorEnum = _reflection.GeneratedProtocolMessageType('UserListLogicalRuleOperatorEnum', (_message.Message,), dict(
  DESCRIPTOR = _USERLISTLOGICALRULEOPERATORENUM,
  __module__ = 'google.ads.googleads_v0.proto.enums.user_list_logical_rule_operator_pb2'
  ,
  __doc__ = """The logical operator of the rule.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.enums.UserListLogicalRuleOperatorEnum)
  ))
_sym_db.RegisterMessage(UserListLogicalRuleOperatorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
