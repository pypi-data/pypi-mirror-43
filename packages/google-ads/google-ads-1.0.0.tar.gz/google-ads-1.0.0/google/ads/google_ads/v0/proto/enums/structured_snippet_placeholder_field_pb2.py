# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/enums/structured_snippet_placeholder_field.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/enums/structured_snippet_placeholder_field.proto',
  package='google.ads.googleads.v0.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v0.enumsB&StructuredSnippetPlaceholderFieldProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v0/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V0.Enums\312\002\035Google\\Ads\\GoogleAds\\V0\\Enums\352\002!Google::Ads::GoogleAds::V0::Enums'),
  serialized_pb=_b('\nNgoogle/ads/googleads_v0/proto/enums/structured_snippet_placeholder_field.proto\x12\x1dgoogle.ads.googleads.v0.enums\"\x84\x01\n%StructuredSnippetPlaceholderFieldEnum\"[\n!StructuredSnippetPlaceholderField\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\n\n\x06HEADER\x10\x02\x12\x0c\n\x08SNIPPETS\x10\x03\x42\xfb\x01\n!com.google.ads.googleads.v0.enumsB&StructuredSnippetPlaceholderFieldProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v0/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V0.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V0\\Enums\xea\x02!Google::Ads::GoogleAds::V0::Enumsb\x06proto3')
)



_STRUCTUREDSNIPPETPLACEHOLDERFIELDENUM_STRUCTUREDSNIPPETPLACEHOLDERFIELD = _descriptor.EnumDescriptor(
  name='StructuredSnippetPlaceholderField',
  full_name='google.ads.googleads.v0.enums.StructuredSnippetPlaceholderFieldEnum.StructuredSnippetPlaceholderField',
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
      name='HEADER', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SNIPPETS', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=155,
  serialized_end=246,
)
_sym_db.RegisterEnumDescriptor(_STRUCTUREDSNIPPETPLACEHOLDERFIELDENUM_STRUCTUREDSNIPPETPLACEHOLDERFIELD)


_STRUCTUREDSNIPPETPLACEHOLDERFIELDENUM = _descriptor.Descriptor(
  name='StructuredSnippetPlaceholderFieldEnum',
  full_name='google.ads.googleads.v0.enums.StructuredSnippetPlaceholderFieldEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _STRUCTUREDSNIPPETPLACEHOLDERFIELDENUM_STRUCTUREDSNIPPETPLACEHOLDERFIELD,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=114,
  serialized_end=246,
)

_STRUCTUREDSNIPPETPLACEHOLDERFIELDENUM_STRUCTUREDSNIPPETPLACEHOLDERFIELD.containing_type = _STRUCTUREDSNIPPETPLACEHOLDERFIELDENUM
DESCRIPTOR.message_types_by_name['StructuredSnippetPlaceholderFieldEnum'] = _STRUCTUREDSNIPPETPLACEHOLDERFIELDENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StructuredSnippetPlaceholderFieldEnum = _reflection.GeneratedProtocolMessageType('StructuredSnippetPlaceholderFieldEnum', (_message.Message,), dict(
  DESCRIPTOR = _STRUCTUREDSNIPPETPLACEHOLDERFIELDENUM,
  __module__ = 'google.ads.googleads_v0.proto.enums.structured_snippet_placeholder_field_pb2'
  ,
  __doc__ = """Values for Structured Snippet placeholder fields.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.enums.StructuredSnippetPlaceholderFieldEnum)
  ))
_sym_db.RegisterMessage(StructuredSnippetPlaceholderFieldEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
