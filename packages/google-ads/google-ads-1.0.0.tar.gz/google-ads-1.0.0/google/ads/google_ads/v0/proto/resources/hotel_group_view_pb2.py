# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/resources/hotel_group_view.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/resources/hotel_group_view.proto',
  package='google.ads.googleads.v0.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v0.resourcesB\023HotelGroupViewProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v0/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V0.Resources\312\002!Google\\Ads\\GoogleAds\\V0\\Resources\352\002%Google::Ads::GoogleAds::V0::Resources'),
  serialized_pb=_b('\n>google/ads/googleads_v0/proto/resources/hotel_group_view.proto\x12!google.ads.googleads.v0.resources\"\'\n\x0eHotelGroupView\x12\x15\n\rresource_name\x18\x01 \x01(\tB\x80\x02\n%com.google.ads.googleads.v0.resourcesB\x13HotelGroupViewProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v0/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V0.Resources\xca\x02!Google\\Ads\\GoogleAds\\V0\\Resources\xea\x02%Google::Ads::GoogleAds::V0::Resourcesb\x06proto3')
)




_HOTELGROUPVIEW = _descriptor.Descriptor(
  name='HotelGroupView',
  full_name='google.ads.googleads.v0.resources.HotelGroupView',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v0.resources.HotelGroupView.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=101,
  serialized_end=140,
)

DESCRIPTOR.message_types_by_name['HotelGroupView'] = _HOTELGROUPVIEW
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HotelGroupView = _reflection.GeneratedProtocolMessageType('HotelGroupView', (_message.Message,), dict(
  DESCRIPTOR = _HOTELGROUPVIEW,
  __module__ = 'google.ads.googleads_v0.proto.resources.hotel_group_view_pb2'
  ,
  __doc__ = """A hotel group view.
  
  
  Attributes:
      resource_name:
          The resource name of the hotel group view. Hotel Group view
          resource names have the form:  ``customers/{customer_id}/hotel
          GroupViews/{ad_group_id}_{criterion_id}``
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.resources.HotelGroupView)
  ))
_sym_db.RegisterMessage(HotelGroupView)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
