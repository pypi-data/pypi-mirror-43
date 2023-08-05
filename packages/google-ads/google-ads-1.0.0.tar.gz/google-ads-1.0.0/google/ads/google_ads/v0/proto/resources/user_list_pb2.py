# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/resources/user_list.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v0.proto.common import user_lists_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_common_dot_user__lists__pb2
from google.ads.google_ads.v0.proto.enums import access_reason_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_access__reason__pb2
from google.ads.google_ads.v0.proto.enums import user_list_access_status_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_user__list__access__status__pb2
from google.ads.google_ads.v0.proto.enums import user_list_closing_reason_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_user__list__closing__reason__pb2
from google.ads.google_ads.v0.proto.enums import user_list_membership_status_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_user__list__membership__status__pb2
from google.ads.google_ads.v0.proto.enums import user_list_size_range_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_user__list__size__range__pb2
from google.ads.google_ads.v0.proto.enums import user_list_type_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_user__list__type__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/resources/user_list.proto',
  package='google.ads.googleads.v0.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v0.resourcesB\rUserListProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v0/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V0.Resources\312\002!Google\\Ads\\GoogleAds\\V0\\Resources\352\002%Google::Ads::GoogleAds::V0::Resources'),
  serialized_pb=_b('\n7google/ads/googleads_v0/proto/resources/user_list.proto\x12!google.ads.googleads.v0.resources\x1a\x35google/ads/googleads_v0/proto/common/user_lists.proto\x1a\x37google/ads/googleads_v0/proto/enums/access_reason.proto\x1a\x41google/ads/googleads_v0/proto/enums/user_list_access_status.proto\x1a\x42google/ads/googleads_v0/proto/enums/user_list_closing_reason.proto\x1a\x45google/ads/googleads_v0/proto/enums/user_list_membership_status.proto\x1a>google/ads/googleads_v0/proto/enums/user_list_size_range.proto\x1a\x38google/ads/googleads_v0/proto/enums/user_list_type.proto\x1a\x1egoogle/protobuf/wrappers.proto\"\x8f\r\n\x08UserList\x12\x15\n\rresource_name\x18\x01 \x01(\t\x12\'\n\x02id\x18\x02 \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12-\n\tread_only\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12*\n\x04name\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\x31\n\x0b\x64\x65scription\x18\x05 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12o\n\x11membership_status\x18\x06 \x01(\x0e\x32T.google.ads.googleads.v0.enums.UserListMembershipStatusEnum.UserListMembershipStatus\x12\x36\n\x10integration_code\x18\x07 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\x39\n\x14membership_life_span\x18\x08 \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12\x35\n\x10size_for_display\x18\t \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12\x66\n\x16size_range_for_display\x18\n \x01(\x0e\x32\x46.google.ads.googleads.v0.enums.UserListSizeRangeEnum.UserListSizeRange\x12\x34\n\x0fsize_for_search\x18\x0b \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12\x65\n\x15size_range_for_search\x18\x0c \x01(\x0e\x32\x46.google.ads.googleads.v0.enums.UserListSizeRangeEnum.UserListSizeRange\x12J\n\x04type\x18\r \x01(\x0e\x32<.google.ads.googleads.v0.enums.UserListTypeEnum.UserListType\x12\x66\n\x0e\x63losing_reason\x18\x0e \x01(\x0e\x32N.google.ads.googleads.v0.enums.UserListClosingReasonEnum.UserListClosingReason\x12S\n\raccess_reason\x18\x0f \x01(\x0e\x32<.google.ads.googleads.v0.enums.AccessReasonEnum.AccessReason\x12n\n\x18\x61\x63\x63ount_user_list_status\x18\x10 \x01(\x0e\x32L.google.ads.googleads.v0.enums.UserListAccessStatusEnum.UserListAccessStatus\x12\x37\n\x13\x65ligible_for_search\x18\x11 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x38\n\x14\x65ligible_for_display\x18\x12 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12S\n\x13\x63rm_based_user_list\x18\x13 \x01(\x0b\x32\x34.google.ads.googleads.v0.common.CrmBasedUserListInfoH\x00\x12P\n\x11similar_user_list\x18\x14 \x01(\x0b\x32\x33.google.ads.googleads.v0.common.SimilarUserListInfoH\x00\x12U\n\x14rule_based_user_list\x18\x15 \x01(\x0b\x32\x35.google.ads.googleads.v0.common.RuleBasedUserListInfoH\x00\x12P\n\x11logical_user_list\x18\x16 \x01(\x0b\x32\x33.google.ads.googleads.v0.common.LogicalUserListInfoH\x00\x12L\n\x0f\x62\x61sic_user_list\x18\x17 \x01(\x0b\x32\x31.google.ads.googleads.v0.common.BasicUserListInfoH\x00\x42\x0b\n\tuser_listB\xfa\x01\n%com.google.ads.googleads.v0.resourcesB\rUserListProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v0/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V0.Resources\xca\x02!Google\\Ads\\GoogleAds\\V0\\Resources\xea\x02%Google::Ads::GoogleAds::V0::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v0_dot_proto_dot_common_dot_user__lists__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_access__reason__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_user__list__access__status__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_user__list__closing__reason__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_user__list__membership__status__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_user__list__size__range__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_user__list__type__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,])




_USERLIST = _descriptor.Descriptor(
  name='UserList',
  full_name='google.ads.googleads.v0.resources.UserList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v0.resources.UserList.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='google.ads.googleads.v0.resources.UserList.id', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='read_only', full_name='google.ads.googleads.v0.resources.UserList.read_only', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='google.ads.googleads.v0.resources.UserList.name', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='google.ads.googleads.v0.resources.UserList.description', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='membership_status', full_name='google.ads.googleads.v0.resources.UserList.membership_status', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='integration_code', full_name='google.ads.googleads.v0.resources.UserList.integration_code', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='membership_life_span', full_name='google.ads.googleads.v0.resources.UserList.membership_life_span', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='size_for_display', full_name='google.ads.googleads.v0.resources.UserList.size_for_display', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='size_range_for_display', full_name='google.ads.googleads.v0.resources.UserList.size_range_for_display', index=9,
      number=10, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='size_for_search', full_name='google.ads.googleads.v0.resources.UserList.size_for_search', index=10,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='size_range_for_search', full_name='google.ads.googleads.v0.resources.UserList.size_range_for_search', index=11,
      number=12, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='google.ads.googleads.v0.resources.UserList.type', index=12,
      number=13, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='closing_reason', full_name='google.ads.googleads.v0.resources.UserList.closing_reason', index=13,
      number=14, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='access_reason', full_name='google.ads.googleads.v0.resources.UserList.access_reason', index=14,
      number=15, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account_user_list_status', full_name='google.ads.googleads.v0.resources.UserList.account_user_list_status', index=15,
      number=16, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='eligible_for_search', full_name='google.ads.googleads.v0.resources.UserList.eligible_for_search', index=16,
      number=17, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='eligible_for_display', full_name='google.ads.googleads.v0.resources.UserList.eligible_for_display', index=17,
      number=18, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='crm_based_user_list', full_name='google.ads.googleads.v0.resources.UserList.crm_based_user_list', index=18,
      number=19, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='similar_user_list', full_name='google.ads.googleads.v0.resources.UserList.similar_user_list', index=19,
      number=20, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rule_based_user_list', full_name='google.ads.googleads.v0.resources.UserList.rule_based_user_list', index=20,
      number=21, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='logical_user_list', full_name='google.ads.googleads.v0.resources.UserList.logical_user_list', index=21,
      number=22, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='basic_user_list', full_name='google.ads.googleads.v0.resources.UserList.basic_user_list', index=22,
      number=23, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='user_list', full_name='google.ads.googleads.v0.resources.UserList.user_list',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=567,
  serialized_end=2246,
)

_USERLIST.fields_by_name['id'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_USERLIST.fields_by_name['read_only'].message_type = google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE
_USERLIST.fields_by_name['name'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_USERLIST.fields_by_name['description'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_USERLIST.fields_by_name['membership_status'].enum_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_user__list__membership__status__pb2._USERLISTMEMBERSHIPSTATUSENUM_USERLISTMEMBERSHIPSTATUS
_USERLIST.fields_by_name['integration_code'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_USERLIST.fields_by_name['membership_life_span'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_USERLIST.fields_by_name['size_for_display'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_USERLIST.fields_by_name['size_range_for_display'].enum_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_user__list__size__range__pb2._USERLISTSIZERANGEENUM_USERLISTSIZERANGE
_USERLIST.fields_by_name['size_for_search'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_USERLIST.fields_by_name['size_range_for_search'].enum_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_user__list__size__range__pb2._USERLISTSIZERANGEENUM_USERLISTSIZERANGE
_USERLIST.fields_by_name['type'].enum_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_user__list__type__pb2._USERLISTTYPEENUM_USERLISTTYPE
_USERLIST.fields_by_name['closing_reason'].enum_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_user__list__closing__reason__pb2._USERLISTCLOSINGREASONENUM_USERLISTCLOSINGREASON
_USERLIST.fields_by_name['access_reason'].enum_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_access__reason__pb2._ACCESSREASONENUM_ACCESSREASON
_USERLIST.fields_by_name['account_user_list_status'].enum_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_user__list__access__status__pb2._USERLISTACCESSSTATUSENUM_USERLISTACCESSSTATUS
_USERLIST.fields_by_name['eligible_for_search'].message_type = google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE
_USERLIST.fields_by_name['eligible_for_display'].message_type = google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE
_USERLIST.fields_by_name['crm_based_user_list'].message_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_common_dot_user__lists__pb2._CRMBASEDUSERLISTINFO
_USERLIST.fields_by_name['similar_user_list'].message_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_common_dot_user__lists__pb2._SIMILARUSERLISTINFO
_USERLIST.fields_by_name['rule_based_user_list'].message_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_common_dot_user__lists__pb2._RULEBASEDUSERLISTINFO
_USERLIST.fields_by_name['logical_user_list'].message_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_common_dot_user__lists__pb2._LOGICALUSERLISTINFO
_USERLIST.fields_by_name['basic_user_list'].message_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_common_dot_user__lists__pb2._BASICUSERLISTINFO
_USERLIST.oneofs_by_name['user_list'].fields.append(
  _USERLIST.fields_by_name['crm_based_user_list'])
_USERLIST.fields_by_name['crm_based_user_list'].containing_oneof = _USERLIST.oneofs_by_name['user_list']
_USERLIST.oneofs_by_name['user_list'].fields.append(
  _USERLIST.fields_by_name['similar_user_list'])
_USERLIST.fields_by_name['similar_user_list'].containing_oneof = _USERLIST.oneofs_by_name['user_list']
_USERLIST.oneofs_by_name['user_list'].fields.append(
  _USERLIST.fields_by_name['rule_based_user_list'])
_USERLIST.fields_by_name['rule_based_user_list'].containing_oneof = _USERLIST.oneofs_by_name['user_list']
_USERLIST.oneofs_by_name['user_list'].fields.append(
  _USERLIST.fields_by_name['logical_user_list'])
_USERLIST.fields_by_name['logical_user_list'].containing_oneof = _USERLIST.oneofs_by_name['user_list']
_USERLIST.oneofs_by_name['user_list'].fields.append(
  _USERLIST.fields_by_name['basic_user_list'])
_USERLIST.fields_by_name['basic_user_list'].containing_oneof = _USERLIST.oneofs_by_name['user_list']
DESCRIPTOR.message_types_by_name['UserList'] = _USERLIST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UserList = _reflection.GeneratedProtocolMessageType('UserList', (_message.Message,), dict(
  DESCRIPTOR = _USERLIST,
  __module__ = 'google.ads.googleads_v0.proto.resources.user_list_pb2'
  ,
  __doc__ = """A user list. This is a list of users a customer may target.
  
  
  Attributes:
      resource_name:
          The resource name of the user list. User list resource names
          have the form:
          ``customers/{customer_id}/userLists/{user_list_id}``
      id:
          Id of the user list.
      read_only:
          A flag that indicates if a user may edit a list. Depends on
          the list ownership and list type. For example, external
          remarketing user lists are not editable.  This field is read-
          only.
      name:
          Name of this user list. Depending on its access\_reason, the
          user list name may not be unique (e.g. if
          access\_reason=SHARED)
      description:
          Description of this user list.
      membership_status:
          Membership status of this user list. Indicates whether a user
          list is open or active. Only open user lists can accumulate
          more users and can be targeted to.
      integration_code:
          An ID from external system. It is used by user list sellers to
          correlate IDs on their systems.
      membership_life_span:
          Number of days a user's cookie stays on your list since its
          most recent addition to the list. This field must be between 0
          and 540 inclusive. However, for CRM based userlists, this
          field can be set to 10000 which means no expiration.  It'll be
          ignored for logical\_user\_list.
      size_for_display:
          Estimated number of users in this user list, on the Google
          Display Network. This value is null if the number of users has
          not yet been determined.  This field is read-only.
      size_range_for_display:
          Size range in terms of number of users of the UserList, on the
          Google Display Network.  This field is read-only.
      size_for_search:
          Estimated number of users in this user list in the google.com
          domain. These are the users available for targeting in Search
          campaigns. This value is null if the number of users has not
          yet been determined.  This field is read-only.
      size_range_for_search:
          Size range in terms of number of users of the UserList, for
          Search ads.  This field is read-only.
      type:
          Type of this list.  This field is read-only.
      closing_reason:
          Indicating the reason why this user list membership status is
          closed. It is only populated on lists that were automatically
          closed due to inactivity, and will be cleared once the list
          membership status becomes open.
      access_reason:
          Indicates the reason this account has been granted access to
          the list. The reason can be SHARED, OWNED, LICENSED or
          SUBSCRIBED.  This field is read-only.
      account_user_list_status:
          Indicates if this share is still enabled. When a UserList is
          shared with the user this field is set to ENABLED. Later the
          userList owner can decide to revoke the share and make it
          DISABLED. The default value of this field is set to ENABLED.
      eligible_for_search:
          Indicates if this user list is eligible for Google Search
          Network.
      eligible_for_display:
          Indicates this user list is eligible for Google Display
          Network.  This field is read-only.
      user_list:
          The user list.  Exactly one must be set.
      crm_based_user_list:
          User list of CRM users provided by the advertiser.
      similar_user_list:
          User list which are similar to users from another UserList.
          These lists are readonly and automatically created by google.
      rule_based_user_list:
          User list generated by a rule.
      logical_user_list:
          User list that is a custom combination of user lists and user
          interests.
      basic_user_list:
          User list targeting as a collection of conversion or
          remarketing actions.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.resources.UserList)
  ))
_sym_db.RegisterMessage(UserList)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
