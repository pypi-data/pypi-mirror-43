# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/services/customer_client_link_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v1.proto.resources import customer_client_link_pb2 as google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_customer__client__link__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v1/proto/services/customer_client_link_service.proto',
  package='google.ads.googleads.v1.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v1.servicesB\036CustomerClientLinkServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v1/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V1.Services\312\002 Google\\Ads\\GoogleAds\\V1\\Services\352\002$Google::Ads::GoogleAds::V1::Services'),
  serialized_pb=_b('\nIgoogle/ads/googleads_v1/proto/services/customer_client_link_service.proto\x12 google.ads.googleads.v1.services\x1a\x42google/ads/googleads_v1/proto/resources/customer_client_link.proto\x1a\x1cgoogle/api/annotations.proto\x1a google/protobuf/field_mask.proto\x1a\x1egoogle/protobuf/wrappers.proto\"5\n\x1cGetCustomerClientLinkRequest\x12\x15\n\rresource_name\x18\x01 \x01(\t\"\x88\x01\n\x1fMutateCustomerClientLinkRequest\x12\x13\n\x0b\x63ustomer_id\x18\x01 \x01(\t\x12P\n\toperation\x18\x02 \x01(\x0b\x32=.google.ads.googleads.v1.services.CustomerClientLinkOperation\"\xed\x01\n\x1b\x43ustomerClientLinkOperation\x12/\n\x0bupdate_mask\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12G\n\x06\x63reate\x18\x01 \x01(\x0b\x32\x35.google.ads.googleads.v1.resources.CustomerClientLinkH\x00\x12G\n\x06update\x18\x02 \x01(\x0b\x32\x35.google.ads.googleads.v1.resources.CustomerClientLinkH\x00\x42\x0b\n\toperation\"t\n MutateCustomerClientLinkResponse\x12P\n\x06result\x18\x01 \x01(\x0b\x32@.google.ads.googleads.v1.services.MutateCustomerClientLinkResult\"7\n\x1eMutateCustomerClientLinkResult\x12\x15\n\rresource_name\x18\x01 \x01(\t2\xd4\x03\n\x19\x43ustomerClientLinkService\x12\xcd\x01\n\x15GetCustomerClientLink\x12>.google.ads.googleads.v1.services.GetCustomerClientLinkRequest\x1a\x35.google.ads.googleads.v1.resources.CustomerClientLink\"=\x82\xd3\xe4\x93\x02\x37\x12\x35/v1/{resource_name=customers/*/customerClientLinks/*}\x12\xe6\x01\n\x18MutateCustomerClientLink\x12\x41.google.ads.googleads.v1.services.MutateCustomerClientLinkRequest\x1a\x42.google.ads.googleads.v1.services.MutateCustomerClientLinkResponse\"C\x82\xd3\xe4\x93\x02=\"8/v1/customers/{customer_id=*}/customerClientLinks:mutate:\x01*B\x85\x02\n$com.google.ads.googleads.v1.servicesB\x1e\x43ustomerClientLinkServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v1/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V1.Services\xca\x02 Google\\Ads\\GoogleAds\\V1\\Services\xea\x02$Google::Ads::GoogleAds::V1::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_customer__client__link__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_protobuf_dot_field__mask__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,])




_GETCUSTOMERCLIENTLINKREQUEST = _descriptor.Descriptor(
  name='GetCustomerClientLinkRequest',
  full_name='google.ads.googleads.v1.services.GetCustomerClientLinkRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v1.services.GetCustomerClientLinkRequest.resource_name', index=0,
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
  serialized_start=275,
  serialized_end=328,
)


_MUTATECUSTOMERCLIENTLINKREQUEST = _descriptor.Descriptor(
  name='MutateCustomerClientLinkRequest',
  full_name='google.ads.googleads.v1.services.MutateCustomerClientLinkRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='customer_id', full_name='google.ads.googleads.v1.services.MutateCustomerClientLinkRequest.customer_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='operation', full_name='google.ads.googleads.v1.services.MutateCustomerClientLinkRequest.operation', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_start=331,
  serialized_end=467,
)


_CUSTOMERCLIENTLINKOPERATION = _descriptor.Descriptor(
  name='CustomerClientLinkOperation',
  full_name='google.ads.googleads.v1.services.CustomerClientLinkOperation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='update_mask', full_name='google.ads.googleads.v1.services.CustomerClientLinkOperation.update_mask', index=0,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='create', full_name='google.ads.googleads.v1.services.CustomerClientLinkOperation.create', index=1,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='update', full_name='google.ads.googleads.v1.services.CustomerClientLinkOperation.update', index=2,
      number=2, type=11, cpp_type=10, label=1,
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
      name='operation', full_name='google.ads.googleads.v1.services.CustomerClientLinkOperation.operation',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=470,
  serialized_end=707,
)


_MUTATECUSTOMERCLIENTLINKRESPONSE = _descriptor.Descriptor(
  name='MutateCustomerClientLinkResponse',
  full_name='google.ads.googleads.v1.services.MutateCustomerClientLinkResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='google.ads.googleads.v1.services.MutateCustomerClientLinkResponse.result', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=709,
  serialized_end=825,
)


_MUTATECUSTOMERCLIENTLINKRESULT = _descriptor.Descriptor(
  name='MutateCustomerClientLinkResult',
  full_name='google.ads.googleads.v1.services.MutateCustomerClientLinkResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v1.services.MutateCustomerClientLinkResult.resource_name', index=0,
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
  serialized_start=827,
  serialized_end=882,
)

_MUTATECUSTOMERCLIENTLINKREQUEST.fields_by_name['operation'].message_type = _CUSTOMERCLIENTLINKOPERATION
_CUSTOMERCLIENTLINKOPERATION.fields_by_name['update_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_CUSTOMERCLIENTLINKOPERATION.fields_by_name['create'].message_type = google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_customer__client__link__pb2._CUSTOMERCLIENTLINK
_CUSTOMERCLIENTLINKOPERATION.fields_by_name['update'].message_type = google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_customer__client__link__pb2._CUSTOMERCLIENTLINK
_CUSTOMERCLIENTLINKOPERATION.oneofs_by_name['operation'].fields.append(
  _CUSTOMERCLIENTLINKOPERATION.fields_by_name['create'])
_CUSTOMERCLIENTLINKOPERATION.fields_by_name['create'].containing_oneof = _CUSTOMERCLIENTLINKOPERATION.oneofs_by_name['operation']
_CUSTOMERCLIENTLINKOPERATION.oneofs_by_name['operation'].fields.append(
  _CUSTOMERCLIENTLINKOPERATION.fields_by_name['update'])
_CUSTOMERCLIENTLINKOPERATION.fields_by_name['update'].containing_oneof = _CUSTOMERCLIENTLINKOPERATION.oneofs_by_name['operation']
_MUTATECUSTOMERCLIENTLINKRESPONSE.fields_by_name['result'].message_type = _MUTATECUSTOMERCLIENTLINKRESULT
DESCRIPTOR.message_types_by_name['GetCustomerClientLinkRequest'] = _GETCUSTOMERCLIENTLINKREQUEST
DESCRIPTOR.message_types_by_name['MutateCustomerClientLinkRequest'] = _MUTATECUSTOMERCLIENTLINKREQUEST
DESCRIPTOR.message_types_by_name['CustomerClientLinkOperation'] = _CUSTOMERCLIENTLINKOPERATION
DESCRIPTOR.message_types_by_name['MutateCustomerClientLinkResponse'] = _MUTATECUSTOMERCLIENTLINKRESPONSE
DESCRIPTOR.message_types_by_name['MutateCustomerClientLinkResult'] = _MUTATECUSTOMERCLIENTLINKRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetCustomerClientLinkRequest = _reflection.GeneratedProtocolMessageType('GetCustomerClientLinkRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETCUSTOMERCLIENTLINKREQUEST,
  __module__ = 'google.ads.googleads_v1.proto.services.customer_client_link_service_pb2'
  ,
  __doc__ = """Request message for
  [CustomerClientLinkService.GetCustomerClientLink][google.ads.googleads.v1.services.CustomerClientLinkService.GetCustomerClientLink].
  
  
  Attributes:
      resource_name:
          The resource name of the customer client link to fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.services.GetCustomerClientLinkRequest)
  ))
_sym_db.RegisterMessage(GetCustomerClientLinkRequest)

MutateCustomerClientLinkRequest = _reflection.GeneratedProtocolMessageType('MutateCustomerClientLinkRequest', (_message.Message,), dict(
  DESCRIPTOR = _MUTATECUSTOMERCLIENTLINKREQUEST,
  __module__ = 'google.ads.googleads_v1.proto.services.customer_client_link_service_pb2'
  ,
  __doc__ = """Request message for
  [CustomerClientLinkService.MutateCustomerClientLink][google.ads.googleads.v1.services.CustomerClientLinkService.MutateCustomerClientLink].
  
  
  Attributes:
      customer_id:
          The ID of the customer whose customer link are being modified.
      operation:
          The operation to perform on the individual CustomerClientLink.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.services.MutateCustomerClientLinkRequest)
  ))
_sym_db.RegisterMessage(MutateCustomerClientLinkRequest)

CustomerClientLinkOperation = _reflection.GeneratedProtocolMessageType('CustomerClientLinkOperation', (_message.Message,), dict(
  DESCRIPTOR = _CUSTOMERCLIENTLINKOPERATION,
  __module__ = 'google.ads.googleads_v1.proto.services.customer_client_link_service_pb2'
  ,
  __doc__ = """A single operation (create, update) on a CustomerClientLink.
  
  
  Attributes:
      update_mask:
          FieldMask that determines which resource fields are modified
          in an update.
      operation:
          The mutate operation.
      create:
          Create operation: No resource name is expected for the new
          link.
      update:
          Update operation: The link is expected to have a valid
          resource name.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.services.CustomerClientLinkOperation)
  ))
_sym_db.RegisterMessage(CustomerClientLinkOperation)

MutateCustomerClientLinkResponse = _reflection.GeneratedProtocolMessageType('MutateCustomerClientLinkResponse', (_message.Message,), dict(
  DESCRIPTOR = _MUTATECUSTOMERCLIENTLINKRESPONSE,
  __module__ = 'google.ads.googleads_v1.proto.services.customer_client_link_service_pb2'
  ,
  __doc__ = """Response message for a CustomerClientLink mutate.
  
  
  Attributes:
      result:
          A result that identifies the resource affected by the mutate
          request.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.services.MutateCustomerClientLinkResponse)
  ))
_sym_db.RegisterMessage(MutateCustomerClientLinkResponse)

MutateCustomerClientLinkResult = _reflection.GeneratedProtocolMessageType('MutateCustomerClientLinkResult', (_message.Message,), dict(
  DESCRIPTOR = _MUTATECUSTOMERCLIENTLINKRESULT,
  __module__ = 'google.ads.googleads_v1.proto.services.customer_client_link_service_pb2'
  ,
  __doc__ = """The result for a single customer client link mutate.
  
  
  Attributes:
      resource_name:
          Returned for successful operations.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.services.MutateCustomerClientLinkResult)
  ))
_sym_db.RegisterMessage(MutateCustomerClientLinkResult)


DESCRIPTOR._options = None

_CUSTOMERCLIENTLINKSERVICE = _descriptor.ServiceDescriptor(
  name='CustomerClientLinkService',
  full_name='google.ads.googleads.v1.services.CustomerClientLinkService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=885,
  serialized_end=1353,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetCustomerClientLink',
    full_name='google.ads.googleads.v1.services.CustomerClientLinkService.GetCustomerClientLink',
    index=0,
    containing_service=None,
    input_type=_GETCUSTOMERCLIENTLINKREQUEST,
    output_type=google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_customer__client__link__pb2._CUSTOMERCLIENTLINK,
    serialized_options=_b('\202\323\344\223\0027\0225/v1/{resource_name=customers/*/customerClientLinks/*}'),
  ),
  _descriptor.MethodDescriptor(
    name='MutateCustomerClientLink',
    full_name='google.ads.googleads.v1.services.CustomerClientLinkService.MutateCustomerClientLink',
    index=1,
    containing_service=None,
    input_type=_MUTATECUSTOMERCLIENTLINKREQUEST,
    output_type=_MUTATECUSTOMERCLIENTLINKRESPONSE,
    serialized_options=_b('\202\323\344\223\002=\"8/v1/customers/{customer_id=*}/customerClientLinks:mutate:\001*'),
  ),
])
_sym_db.RegisterServiceDescriptor(_CUSTOMERCLIENTLINKSERVICE)

DESCRIPTOR.services_by_name['CustomerClientLinkService'] = _CUSTOMERCLIENTLINKSERVICE

# @@protoc_insertion_point(module_scope)
