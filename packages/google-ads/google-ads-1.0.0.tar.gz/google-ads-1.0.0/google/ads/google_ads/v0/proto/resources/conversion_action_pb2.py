# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/resources/conversion_action.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v0.proto.common import tag_snippet_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_common_dot_tag__snippet__pb2
from google.ads.google_ads.v0.proto.enums import attribution_model_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_attribution__model__pb2
from google.ads.google_ads.v0.proto.enums import conversion_action_category_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_conversion__action__category__pb2
from google.ads.google_ads.v0.proto.enums import conversion_action_counting_type_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_conversion__action__counting__type__pb2
from google.ads.google_ads.v0.proto.enums import conversion_action_status_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_conversion__action__status__pb2
from google.ads.google_ads.v0.proto.enums import conversion_action_type_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_conversion__action__type__pb2
from google.ads.google_ads.v0.proto.enums import data_driven_model_status_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_data__driven__model__status__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/resources/conversion_action.proto',
  package='google.ads.googleads.v0.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v0.resourcesB\025ConversionActionProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v0/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V0.Resources\312\002!Google\\Ads\\GoogleAds\\V0\\Resources\352\002%Google::Ads::GoogleAds::V0::Resources'),
  serialized_pb=_b('\n?google/ads/googleads_v0/proto/resources/conversion_action.proto\x12!google.ads.googleads.v0.resources\x1a\x36google/ads/googleads_v0/proto/common/tag_snippet.proto\x1a;google/ads/googleads_v0/proto/enums/attribution_model.proto\x1a\x44google/ads/googleads_v0/proto/enums/conversion_action_category.proto\x1aIgoogle/ads/googleads_v0/proto/enums/conversion_action_counting_type.proto\x1a\x42google/ads/googleads_v0/proto/enums/conversion_action_status.proto\x1a@google/ads/googleads_v0/proto/enums/conversion_action_type.proto\x1a\x42google/ads/googleads_v0/proto/enums/data_driven_model_status.proto\x1a\x1egoogle/protobuf/wrappers.proto\"\xd4\x0c\n\x10\x43onversionAction\x12\x15\n\rresource_name\x18\x01 \x01(\t\x12\'\n\x02id\x18\x02 \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12*\n\x04name\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12`\n\x06status\x18\x04 \x01(\x0e\x32P.google.ads.googleads.v0.enums.ConversionActionStatusEnum.ConversionActionStatus\x12Z\n\x04type\x18\x05 \x01(\x0e\x32L.google.ads.googleads.v0.enums.ConversionActionTypeEnum.ConversionActionType\x12\x66\n\x08\x63\x61tegory\x18\x06 \x01(\x0e\x32T.google.ads.googleads.v0.enums.ConversionActionCategoryEnum.ConversionActionCategory\x12\x34\n\x0eowner_customer\x18\x07 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\x41\n\x1dinclude_in_conversions_metric\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12G\n\"click_through_lookback_window_days\x18\t \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12\x46\n!view_through_lookback_window_days\x18\n \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12Y\n\x0evalue_settings\x18\x0b \x01(\x0b\x32\x41.google.ads.googleads.v0.resources.ConversionAction.ValueSettings\x12s\n\rcounting_type\x18\x0c \x01(\x0e\x32\\.google.ads.googleads.v0.enums.ConversionActionCountingTypeEnum.ConversionActionCountingType\x12p\n\x1a\x61ttribution_model_settings\x18\r \x01(\x0b\x32L.google.ads.googleads.v0.resources.ConversionAction.AttributionModelSettings\x12@\n\x0ctag_snippets\x18\x0e \x03(\x0b\x32*.google.ads.googleads.v0.common.TagSnippet\x12@\n\x1bphone_call_duration_seconds\x18\x0f \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12,\n\x06\x61pp_id\x18\x10 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x1a\xed\x01\n\x18\x41ttributionModelSettings\x12_\n\x11\x61ttribution_model\x18\x01 \x01(\x0e\x32\x44.google.ads.googleads.v0.enums.AttributionModelEnum.AttributionModel\x12p\n\x18\x64\x61ta_driven_model_status\x18\x02 \x01(\x0e\x32N.google.ads.googleads.v0.enums.DataDrivenModelStatusEnum.DataDrivenModelStatus\x1a\xbf\x01\n\rValueSettings\x12\x33\n\rdefault_value\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12;\n\x15\x64\x65\x66\x61ult_currency_code\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12<\n\x18\x61lways_use_default_value\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.BoolValueB\x82\x02\n%com.google.ads.googleads.v0.resourcesB\x15\x43onversionActionProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v0/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V0.Resources\xca\x02!Google\\Ads\\GoogleAds\\V0\\Resources\xea\x02%Google::Ads::GoogleAds::V0::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v0_dot_proto_dot_common_dot_tag__snippet__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_attribution__model__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_conversion__action__category__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_conversion__action__counting__type__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_conversion__action__status__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_conversion__action__type__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_data__driven__model__status__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,])




_CONVERSIONACTION_ATTRIBUTIONMODELSETTINGS = _descriptor.Descriptor(
  name='AttributionModelSettings',
  full_name='google.ads.googleads.v0.resources.ConversionAction.AttributionModelSettings',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='attribution_model', full_name='google.ads.googleads.v0.resources.ConversionAction.AttributionModelSettings.attribution_model', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data_driven_model_status', full_name='google.ads.googleads.v0.resources.ConversionAction.AttributionModelSettings.data_driven_model_status', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
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
  ],
  serialized_start=1788,
  serialized_end=2025,
)

_CONVERSIONACTION_VALUESETTINGS = _descriptor.Descriptor(
  name='ValueSettings',
  full_name='google.ads.googleads.v0.resources.ConversionAction.ValueSettings',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='default_value', full_name='google.ads.googleads.v0.resources.ConversionAction.ValueSettings.default_value', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='default_currency_code', full_name='google.ads.googleads.v0.resources.ConversionAction.ValueSettings.default_currency_code', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='always_use_default_value', full_name='google.ads.googleads.v0.resources.ConversionAction.ValueSettings.always_use_default_value', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  ],
  serialized_start=2028,
  serialized_end=2219,
)

_CONVERSIONACTION = _descriptor.Descriptor(
  name='ConversionAction',
  full_name='google.ads.googleads.v0.resources.ConversionAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v0.resources.ConversionAction.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='google.ads.googleads.v0.resources.ConversionAction.id', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='google.ads.googleads.v0.resources.ConversionAction.name', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='google.ads.googleads.v0.resources.ConversionAction.status', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='google.ads.googleads.v0.resources.ConversionAction.type', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='category', full_name='google.ads.googleads.v0.resources.ConversionAction.category', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='owner_customer', full_name='google.ads.googleads.v0.resources.ConversionAction.owner_customer', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='include_in_conversions_metric', full_name='google.ads.googleads.v0.resources.ConversionAction.include_in_conversions_metric', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='click_through_lookback_window_days', full_name='google.ads.googleads.v0.resources.ConversionAction.click_through_lookback_window_days', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='view_through_lookback_window_days', full_name='google.ads.googleads.v0.resources.ConversionAction.view_through_lookback_window_days', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value_settings', full_name='google.ads.googleads.v0.resources.ConversionAction.value_settings', index=10,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='counting_type', full_name='google.ads.googleads.v0.resources.ConversionAction.counting_type', index=11,
      number=12, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='attribution_model_settings', full_name='google.ads.googleads.v0.resources.ConversionAction.attribution_model_settings', index=12,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tag_snippets', full_name='google.ads.googleads.v0.resources.ConversionAction.tag_snippets', index=13,
      number=14, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='phone_call_duration_seconds', full_name='google.ads.googleads.v0.resources.ConversionAction.phone_call_duration_seconds', index=14,
      number=15, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='app_id', full_name='google.ads.googleads.v0.resources.ConversionAction.app_id', index=15,
      number=16, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_CONVERSIONACTION_ATTRIBUTIONMODELSETTINGS, _CONVERSIONACTION_VALUESETTINGS, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=599,
  serialized_end=2219,
)

_CONVERSIONACTION_ATTRIBUTIONMODELSETTINGS.fields_by_name['attribution_model'].enum_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_attribution__model__pb2._ATTRIBUTIONMODELENUM_ATTRIBUTIONMODEL
_CONVERSIONACTION_ATTRIBUTIONMODELSETTINGS.fields_by_name['data_driven_model_status'].enum_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_data__driven__model__status__pb2._DATADRIVENMODELSTATUSENUM_DATADRIVENMODELSTATUS
_CONVERSIONACTION_ATTRIBUTIONMODELSETTINGS.containing_type = _CONVERSIONACTION
_CONVERSIONACTION_VALUESETTINGS.fields_by_name['default_value'].message_type = google_dot_protobuf_dot_wrappers__pb2._DOUBLEVALUE
_CONVERSIONACTION_VALUESETTINGS.fields_by_name['default_currency_code'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CONVERSIONACTION_VALUESETTINGS.fields_by_name['always_use_default_value'].message_type = google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE
_CONVERSIONACTION_VALUESETTINGS.containing_type = _CONVERSIONACTION
_CONVERSIONACTION.fields_by_name['id'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_CONVERSIONACTION.fields_by_name['name'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CONVERSIONACTION.fields_by_name['status'].enum_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_conversion__action__status__pb2._CONVERSIONACTIONSTATUSENUM_CONVERSIONACTIONSTATUS
_CONVERSIONACTION.fields_by_name['type'].enum_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_conversion__action__type__pb2._CONVERSIONACTIONTYPEENUM_CONVERSIONACTIONTYPE
_CONVERSIONACTION.fields_by_name['category'].enum_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_conversion__action__category__pb2._CONVERSIONACTIONCATEGORYENUM_CONVERSIONACTIONCATEGORY
_CONVERSIONACTION.fields_by_name['owner_customer'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CONVERSIONACTION.fields_by_name['include_in_conversions_metric'].message_type = google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE
_CONVERSIONACTION.fields_by_name['click_through_lookback_window_days'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_CONVERSIONACTION.fields_by_name['view_through_lookback_window_days'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_CONVERSIONACTION.fields_by_name['value_settings'].message_type = _CONVERSIONACTION_VALUESETTINGS
_CONVERSIONACTION.fields_by_name['counting_type'].enum_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_enums_dot_conversion__action__counting__type__pb2._CONVERSIONACTIONCOUNTINGTYPEENUM_CONVERSIONACTIONCOUNTINGTYPE
_CONVERSIONACTION.fields_by_name['attribution_model_settings'].message_type = _CONVERSIONACTION_ATTRIBUTIONMODELSETTINGS
_CONVERSIONACTION.fields_by_name['tag_snippets'].message_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_common_dot_tag__snippet__pb2._TAGSNIPPET
_CONVERSIONACTION.fields_by_name['phone_call_duration_seconds'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_CONVERSIONACTION.fields_by_name['app_id'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
DESCRIPTOR.message_types_by_name['ConversionAction'] = _CONVERSIONACTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ConversionAction = _reflection.GeneratedProtocolMessageType('ConversionAction', (_message.Message,), dict(

  AttributionModelSettings = _reflection.GeneratedProtocolMessageType('AttributionModelSettings', (_message.Message,), dict(
    DESCRIPTOR = _CONVERSIONACTION_ATTRIBUTIONMODELSETTINGS,
    __module__ = 'google.ads.googleads_v0.proto.resources.conversion_action_pb2'
    ,
    __doc__ = """Settings related to this conversion action's attribution model.
    
    
    Attributes:
        attribution_model:
            The attribution model type of this conversion action.
        data_driven_model_status:
            The status of the data-driven attribution model for the
            conversion action.
    """,
    # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.resources.ConversionAction.AttributionModelSettings)
    ))
  ,

  ValueSettings = _reflection.GeneratedProtocolMessageType('ValueSettings', (_message.Message,), dict(
    DESCRIPTOR = _CONVERSIONACTION_VALUESETTINGS,
    __module__ = 'google.ads.googleads_v0.proto.resources.conversion_action_pb2'
    ,
    __doc__ = """Settings related to the value for conversion events associated with this
    conversion action.
    
    
    Attributes:
        default_value:
            The value to use when conversion events for this conversion
            action are sent with an invalid, disallowed or missing value,
            or when this conversion action is configured to always use the
            default value.
        default_currency_code:
            The currency code to use when conversion events for this
            conversion action are sent with an invalid or missing currency
            code, or when this conversion action is configured to always
            use the default value.
        always_use_default_value:
            Controls whether the default value and default currency code
            are used in place of the value and currency code specified in
            conversion events for this conversion action.
    """,
    # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.resources.ConversionAction.ValueSettings)
    ))
  ,
  DESCRIPTOR = _CONVERSIONACTION,
  __module__ = 'google.ads.googleads_v0.proto.resources.conversion_action_pb2'
  ,
  __doc__ = """A conversion action.
  
  
  Attributes:
      resource_name:
          The resource name of the conversion action. Conversion action
          resource names have the form:  ``customers/{customer_id}/conve
          rsionActions/{conversion_action_id}``
      id:
          The ID of the conversion action.
      name:
          The name of the conversion action.  This field is required and
          should not be empty when creating new conversion actions.
      status:
          The status of this conversion action for conversion event
          accrual.
      type:
          The type of this conversion action.
      category:
          The category of conversions reported for this conversion
          action.
      owner_customer:
          The resource name of the conversion action owner customer, or
          null if this is a system-defined conversion action.
      include_in_conversions_metric:
          Whether this conversion action should be included in the
          "conversions" metric.
      click_through_lookback_window_days:
          The maximum number of days that may elapse between an
          interaction (e.g., a click) and a conversion event.
      view_through_lookback_window_days:
          The maximum number of days which may elapse between an
          impression and a conversion without an interaction.
      value_settings:
          Settings related to the value for conversion events associated
          with this conversion action.
      counting_type:
          How to count conversion events for the conversion action.
      attribution_model_settings:
          Settings related to this conversion action's attribution
          model.
      tag_snippets:
          The snippets used for tracking conversions.
      phone_call_duration_seconds:
          The phone call duration in seconds after which a conversion
          should be reported for this conversion action.  The value must
          be between 0 and 10000, inclusive.
      app_id:
          App ID for an app conversion action.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.resources.ConversionAction)
  ))
_sym_db.RegisterMessage(ConversionAction)
_sym_db.RegisterMessage(ConversionAction.AttributionModelSettings)
_sym_db.RegisterMessage(ConversionAction.ValueSettings)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
