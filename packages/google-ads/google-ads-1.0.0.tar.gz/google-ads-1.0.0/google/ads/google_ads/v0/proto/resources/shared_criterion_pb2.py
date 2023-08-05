# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/resources/shared_criterion.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v0.proto.common import criteria_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_common_dot_criteria__pb2
from google.ads.google_ads.v0.proto.enums import criterion_type_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_criterion__type__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/resources/shared_criterion.proto',
  package='google.ads.googleads.v0.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v0.resourcesB\024SharedCriterionProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v0/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V0.Resources\312\002!Google\\Ads\\GoogleAds\\V0\\Resources\352\002%Google::Ads::GoogleAds::V0::Resources'),
  serialized_pb=_b('\n>google/ads/googleads_v0/proto/resources/shared_criterion.proto\x12!google.ads.googleads.v0.resources\x1a\x33google/ads/googleads_v0/proto/common/criteria.proto\x1a\x38google/ads/googleads_v0/proto/enums/criterion_type.proto\x1a\x1egoogle/protobuf/wrappers.proto\"\xdc\x04\n\x0fSharedCriterion\x12\x15\n\rresource_name\x18\x01 \x01(\t\x12\x30\n\nshared_set\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\x31\n\x0c\x63riterion_id\x18\x1a \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12L\n\x04type\x18\x04 \x01(\x0e\x32>.google.ads.googleads.v0.enums.CriterionTypeEnum.CriterionType\x12>\n\x07keyword\x18\x03 \x01(\x0b\x32+.google.ads.googleads.v0.common.KeywordInfoH\x00\x12I\n\ryoutube_video\x18\x05 \x01(\x0b\x32\x30.google.ads.googleads.v0.common.YouTubeVideoInfoH\x00\x12M\n\x0fyoutube_channel\x18\x06 \x01(\x0b\x32\x32.google.ads.googleads.v0.common.YouTubeChannelInfoH\x00\x12\x42\n\tplacement\x18\x07 \x01(\x0b\x32-.google.ads.googleads.v0.common.PlacementInfoH\x00\x12T\n\x13mobile_app_category\x18\x08 \x01(\x0b\x32\x35.google.ads.googleads.v0.common.MobileAppCategoryInfoH\x00\x42\x0b\n\tcriterionB\x81\x02\n%com.google.ads.googleads.v0.resourcesB\x14SharedCriterionProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v0/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V0.Resources\xca\x02!Google\\Ads\\GoogleAds\\V0\\Resources\xea\x02%Google::Ads::GoogleAds::V0::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v0_dot_proto_dot_common_dot_criteria__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_criterion__type__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,])




_SHAREDCRITERION = _descriptor.Descriptor(
  name='SharedCriterion',
  full_name='google.ads.googleads.v0.resources.SharedCriterion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v0.resources.SharedCriterion.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shared_set', full_name='google.ads.googleads.v0.resources.SharedCriterion.shared_set', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='criterion_id', full_name='google.ads.googleads.v0.resources.SharedCriterion.criterion_id', index=2,
      number=26, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='google.ads.googleads.v0.resources.SharedCriterion.type', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='keyword', full_name='google.ads.googleads.v0.resources.SharedCriterion.keyword', index=4,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='youtube_video', full_name='google.ads.googleads.v0.resources.SharedCriterion.youtube_video', index=5,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='youtube_channel', full_name='google.ads.googleads.v0.resources.SharedCriterion.youtube_channel', index=6,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='placement', full_name='google.ads.googleads.v0.resources.SharedCriterion.placement', index=7,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mobile_app_category', full_name='google.ads.googleads.v0.resources.SharedCriterion.mobile_app_category', index=8,
      number=8, type=11, cpp_type=10, label=1,
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
      name='criterion', full_name='google.ads.googleads.v0.resources.SharedCriterion.criterion',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=245,
  serialized_end=849,
)

_SHAREDCRITERION.fields_by_name['shared_set'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_SHAREDCRITERION.fields_by_name['criterion_id'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_SHAREDCRITERION.fields_by_name['type'].enum_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_criterion__type__pb2._CRITERIONTYPEENUM_CRITERIONTYPE
_SHAREDCRITERION.fields_by_name['keyword'].message_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_common_dot_criteria__pb2._KEYWORDINFO
_SHAREDCRITERION.fields_by_name['youtube_video'].message_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_common_dot_criteria__pb2._YOUTUBEVIDEOINFO
_SHAREDCRITERION.fields_by_name['youtube_channel'].message_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_common_dot_criteria__pb2._YOUTUBECHANNELINFO
_SHAREDCRITERION.fields_by_name['placement'].message_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_common_dot_criteria__pb2._PLACEMENTINFO
_SHAREDCRITERION.fields_by_name['mobile_app_category'].message_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_common_dot_criteria__pb2._MOBILEAPPCATEGORYINFO
_SHAREDCRITERION.oneofs_by_name['criterion'].fields.append(
  _SHAREDCRITERION.fields_by_name['keyword'])
_SHAREDCRITERION.fields_by_name['keyword'].containing_oneof = _SHAREDCRITERION.oneofs_by_name['criterion']
_SHAREDCRITERION.oneofs_by_name['criterion'].fields.append(
  _SHAREDCRITERION.fields_by_name['youtube_video'])
_SHAREDCRITERION.fields_by_name['youtube_video'].containing_oneof = _SHAREDCRITERION.oneofs_by_name['criterion']
_SHAREDCRITERION.oneofs_by_name['criterion'].fields.append(
  _SHAREDCRITERION.fields_by_name['youtube_channel'])
_SHAREDCRITERION.fields_by_name['youtube_channel'].containing_oneof = _SHAREDCRITERION.oneofs_by_name['criterion']
_SHAREDCRITERION.oneofs_by_name['criterion'].fields.append(
  _SHAREDCRITERION.fields_by_name['placement'])
_SHAREDCRITERION.fields_by_name['placement'].containing_oneof = _SHAREDCRITERION.oneofs_by_name['criterion']
_SHAREDCRITERION.oneofs_by_name['criterion'].fields.append(
  _SHAREDCRITERION.fields_by_name['mobile_app_category'])
_SHAREDCRITERION.fields_by_name['mobile_app_category'].containing_oneof = _SHAREDCRITERION.oneofs_by_name['criterion']
DESCRIPTOR.message_types_by_name['SharedCriterion'] = _SHAREDCRITERION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SharedCriterion = _reflection.GeneratedProtocolMessageType('SharedCriterion', (_message.Message,), dict(
  DESCRIPTOR = _SHAREDCRITERION,
  __module__ = 'google.ads.googleads_v0.proto.resources.shared_criterion_pb2'
  ,
  __doc__ = """A criterion belonging to a shared set.
  
  
  Attributes:
      resource_name:
          The resource name of the shared criterion. Shared set resource
          names have the form:  ``customers/{customer_id}/sharedCriteria
          /{shared_set_id}_{criterion_id}``
      shared_set:
          The shared set to which the shared criterion belongs.
      criterion_id:
          The ID of the criterion.  This field is ignored for mutates.
      type:
          The type of the criterion.
      criterion:
          The criterion.  Exactly one must be set.
      keyword:
          Keyword.
      youtube_video:
          YouTube Video.
      youtube_channel:
          YouTube Channel.
      placement:
          Placement.
      mobile_app_category:
          Mobile App Category.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.resources.SharedCriterion)
  ))
_sym_db.RegisterMessage(SharedCriterion)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
