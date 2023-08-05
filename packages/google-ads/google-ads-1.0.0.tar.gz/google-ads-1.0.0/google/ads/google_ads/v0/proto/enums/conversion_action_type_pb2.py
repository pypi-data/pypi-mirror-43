# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/enums/conversion_action_type.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/enums/conversion_action_type.proto',
  package='google.ads.googleads.v0.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v0.enumsB\031ConversionActionTypeProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v0/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V0.Enums\312\002\035Google\\Ads\\GoogleAds\\V0\\Enums\352\002!Google::Ads::GoogleAds::V0::Enums'),
  serialized_pb=_b('\n@google/ads/googleads_v0/proto/enums/conversion_action_type.proto\x12\x1dgoogle.ads.googleads.v0.enums\"\xf0\x01\n\x18\x43onversionActionTypeEnum\"\xd3\x01\n\x14\x43onversionActionType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0b\n\x07\x41\x44_CALL\x10\x02\x12\x11\n\rCLICK_TO_CALL\x10\x03\x12\x18\n\x14GOOGLE_PLAY_DOWNLOAD\x10\x04\x12\x1f\n\x1bGOOGLE_PLAY_IN_APP_PURCHASE\x10\x05\x12\x10\n\x0cUPLOAD_CALLS\x10\x06\x12\x11\n\rUPLOAD_CLICKS\x10\x07\x12\x0b\n\x07WEBPAGE\x10\x08\x12\x10\n\x0cWEBSITE_CALL\x10\tB\xee\x01\n!com.google.ads.googleads.v0.enumsB\x19\x43onversionActionTypeProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v0/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V0.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V0\\Enums\xea\x02!Google::Ads::GoogleAds::V0::Enumsb\x06proto3')
)



_CONVERSIONACTIONTYPEENUM_CONVERSIONACTIONTYPE = _descriptor.EnumDescriptor(
  name='ConversionActionType',
  full_name='google.ads.googleads.v0.enums.ConversionActionTypeEnum.ConversionActionType',
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
      name='AD_CALL', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CLICK_TO_CALL', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GOOGLE_PLAY_DOWNLOAD', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GOOGLE_PLAY_IN_APP_PURCHASE', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UPLOAD_CALLS', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UPLOAD_CLICKS', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WEBPAGE', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WEBSITE_CALL', index=9, number=9,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=129,
  serialized_end=340,
)
_sym_db.RegisterEnumDescriptor(_CONVERSIONACTIONTYPEENUM_CONVERSIONACTIONTYPE)


_CONVERSIONACTIONTYPEENUM = _descriptor.Descriptor(
  name='ConversionActionTypeEnum',
  full_name='google.ads.googleads.v0.enums.ConversionActionTypeEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CONVERSIONACTIONTYPEENUM_CONVERSIONACTIONTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=100,
  serialized_end=340,
)

_CONVERSIONACTIONTYPEENUM_CONVERSIONACTIONTYPE.containing_type = _CONVERSIONACTIONTYPEENUM
DESCRIPTOR.message_types_by_name['ConversionActionTypeEnum'] = _CONVERSIONACTIONTYPEENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ConversionActionTypeEnum = _reflection.GeneratedProtocolMessageType('ConversionActionTypeEnum', (_message.Message,), dict(
  DESCRIPTOR = _CONVERSIONACTIONTYPEENUM,
  __module__ = 'google.ads.googleads_v0.proto.enums.conversion_action_type_pb2'
  ,
  __doc__ = """Container for enum describing possible types of a conversion action.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.enums.ConversionActionTypeEnum)
  ))
_sym_db.RegisterMessage(ConversionActionTypeEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
