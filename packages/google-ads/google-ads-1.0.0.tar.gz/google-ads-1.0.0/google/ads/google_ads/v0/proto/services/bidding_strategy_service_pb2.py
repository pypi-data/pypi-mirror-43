# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/services/bidding_strategy_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v0.proto.resources import bidding_strategy_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_resources_dot_bidding__strategy__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.rpc import status_pb2 as google_dot_rpc_dot_status__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/services/bidding_strategy_service.proto',
  package='google.ads.googleads.v0.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v0.servicesB\033BiddingStrategyServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v0/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V0.Services\312\002 Google\\Ads\\GoogleAds\\V0\\Services\352\002$Google::Ads::GoogleAds::V0::Services'),
  serialized_pb=_b('\nEgoogle/ads/googleads_v0/proto/services/bidding_strategy_service.proto\x12 google.ads.googleads.v0.services\x1a>google/ads/googleads_v0/proto/resources/bidding_strategy.proto\x1a\x1cgoogle/api/annotations.proto\x1a google/protobuf/field_mask.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x17google/rpc/status.proto\"2\n\x19GetBiddingStrategyRequest\x12\x15\n\rresource_name\x18\x01 \x01(\t\"\xb5\x01\n\x1eMutateBiddingStrategiesRequest\x12\x13\n\x0b\x63ustomer_id\x18\x01 \x01(\t\x12N\n\noperations\x18\x02 \x03(\x0b\x32:.google.ads.googleads.v0.services.BiddingStrategyOperation\x12\x17\n\x0fpartial_failure\x18\x03 \x01(\x08\x12\x15\n\rvalidate_only\x18\x04 \x01(\x08\"\xf6\x01\n\x18\x42iddingStrategyOperation\x12/\n\x0bupdate_mask\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12\x44\n\x06\x63reate\x18\x01 \x01(\x0b\x32\x32.google.ads.googleads.v0.resources.BiddingStrategyH\x00\x12\x44\n\x06update\x18\x02 \x01(\x0b\x32\x32.google.ads.googleads.v0.resources.BiddingStrategyH\x00\x12\x10\n\x06remove\x18\x03 \x01(\tH\x00\x42\x0b\n\toperation\"\xa4\x01\n\x1fMutateBiddingStrategiesResponse\x12\x31\n\x15partial_failure_error\x18\x03 \x01(\x0b\x32\x12.google.rpc.Status\x12N\n\x07results\x18\x02 \x03(\x0b\x32=.google.ads.googleads.v0.services.MutateBiddingStrategyResult\"4\n\x1bMutateBiddingStrategyResult\x12\x15\n\rresource_name\x18\x01 \x01(\t2\xc1\x03\n\x16\x42iddingStrategyService\x12\xc2\x01\n\x12GetBiddingStrategy\x12;.google.ads.googleads.v0.services.GetBiddingStrategyRequest\x1a\x32.google.ads.googleads.v0.resources.BiddingStrategy\";\x82\xd3\xe4\x93\x02\x35\x12\x33/v0/{resource_name=customers/*/biddingStrategies/*}\x12\xe1\x01\n\x17MutateBiddingStrategies\x12@.google.ads.googleads.v0.services.MutateBiddingStrategiesRequest\x1a\x41.google.ads.googleads.v0.services.MutateBiddingStrategiesResponse\"A\x82\xd3\xe4\x93\x02;\"6/v0/customers/{customer_id=*}/biddingStrategies:mutate:\x01*B\x82\x02\n$com.google.ads.googleads.v0.servicesB\x1b\x42iddingStrategyServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v0/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V0.Services\xca\x02 Google\\Ads\\GoogleAds\\V0\\Services\xea\x02$Google::Ads::GoogleAds::V0::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v0_dot_proto_dot_resources_dot_bidding__strategy__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_protobuf_dot_field__mask__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_rpc_dot_status__pb2.DESCRIPTOR,])




_GETBIDDINGSTRATEGYREQUEST = _descriptor.Descriptor(
  name='GetBiddingStrategyRequest',
  full_name='google.ads.googleads.v0.services.GetBiddingStrategyRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v0.services.GetBiddingStrategyRequest.resource_name', index=0,
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
  serialized_start=292,
  serialized_end=342,
)


_MUTATEBIDDINGSTRATEGIESREQUEST = _descriptor.Descriptor(
  name='MutateBiddingStrategiesRequest',
  full_name='google.ads.googleads.v0.services.MutateBiddingStrategiesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='customer_id', full_name='google.ads.googleads.v0.services.MutateBiddingStrategiesRequest.customer_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='operations', full_name='google.ads.googleads.v0.services.MutateBiddingStrategiesRequest.operations', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='partial_failure', full_name='google.ads.googleads.v0.services.MutateBiddingStrategiesRequest.partial_failure', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='validate_only', full_name='google.ads.googleads.v0.services.MutateBiddingStrategiesRequest.validate_only', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=345,
  serialized_end=526,
)


_BIDDINGSTRATEGYOPERATION = _descriptor.Descriptor(
  name='BiddingStrategyOperation',
  full_name='google.ads.googleads.v0.services.BiddingStrategyOperation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='update_mask', full_name='google.ads.googleads.v0.services.BiddingStrategyOperation.update_mask', index=0,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='create', full_name='google.ads.googleads.v0.services.BiddingStrategyOperation.create', index=1,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='update', full_name='google.ads.googleads.v0.services.BiddingStrategyOperation.update', index=2,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='remove', full_name='google.ads.googleads.v0.services.BiddingStrategyOperation.remove', index=3,
      number=3, type=9, cpp_type=9, label=1,
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
    _descriptor.OneofDescriptor(
      name='operation', full_name='google.ads.googleads.v0.services.BiddingStrategyOperation.operation',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=529,
  serialized_end=775,
)


_MUTATEBIDDINGSTRATEGIESRESPONSE = _descriptor.Descriptor(
  name='MutateBiddingStrategiesResponse',
  full_name='google.ads.googleads.v0.services.MutateBiddingStrategiesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='partial_failure_error', full_name='google.ads.googleads.v0.services.MutateBiddingStrategiesResponse.partial_failure_error', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='results', full_name='google.ads.googleads.v0.services.MutateBiddingStrategiesResponse.results', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=778,
  serialized_end=942,
)


_MUTATEBIDDINGSTRATEGYRESULT = _descriptor.Descriptor(
  name='MutateBiddingStrategyResult',
  full_name='google.ads.googleads.v0.services.MutateBiddingStrategyResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v0.services.MutateBiddingStrategyResult.resource_name', index=0,
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
  serialized_start=944,
  serialized_end=996,
)

_MUTATEBIDDINGSTRATEGIESREQUEST.fields_by_name['operations'].message_type = _BIDDINGSTRATEGYOPERATION
_BIDDINGSTRATEGYOPERATION.fields_by_name['update_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_BIDDINGSTRATEGYOPERATION.fields_by_name['create'].message_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_resources_dot_bidding__strategy__pb2._BIDDINGSTRATEGY
_BIDDINGSTRATEGYOPERATION.fields_by_name['update'].message_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_resources_dot_bidding__strategy__pb2._BIDDINGSTRATEGY
_BIDDINGSTRATEGYOPERATION.oneofs_by_name['operation'].fields.append(
  _BIDDINGSTRATEGYOPERATION.fields_by_name['create'])
_BIDDINGSTRATEGYOPERATION.fields_by_name['create'].containing_oneof = _BIDDINGSTRATEGYOPERATION.oneofs_by_name['operation']
_BIDDINGSTRATEGYOPERATION.oneofs_by_name['operation'].fields.append(
  _BIDDINGSTRATEGYOPERATION.fields_by_name['update'])
_BIDDINGSTRATEGYOPERATION.fields_by_name['update'].containing_oneof = _BIDDINGSTRATEGYOPERATION.oneofs_by_name['operation']
_BIDDINGSTRATEGYOPERATION.oneofs_by_name['operation'].fields.append(
  _BIDDINGSTRATEGYOPERATION.fields_by_name['remove'])
_BIDDINGSTRATEGYOPERATION.fields_by_name['remove'].containing_oneof = _BIDDINGSTRATEGYOPERATION.oneofs_by_name['operation']
_MUTATEBIDDINGSTRATEGIESRESPONSE.fields_by_name['partial_failure_error'].message_type = google_dot_rpc_dot_status__pb2._STATUS
_MUTATEBIDDINGSTRATEGIESRESPONSE.fields_by_name['results'].message_type = _MUTATEBIDDINGSTRATEGYRESULT
DESCRIPTOR.message_types_by_name['GetBiddingStrategyRequest'] = _GETBIDDINGSTRATEGYREQUEST
DESCRIPTOR.message_types_by_name['MutateBiddingStrategiesRequest'] = _MUTATEBIDDINGSTRATEGIESREQUEST
DESCRIPTOR.message_types_by_name['BiddingStrategyOperation'] = _BIDDINGSTRATEGYOPERATION
DESCRIPTOR.message_types_by_name['MutateBiddingStrategiesResponse'] = _MUTATEBIDDINGSTRATEGIESRESPONSE
DESCRIPTOR.message_types_by_name['MutateBiddingStrategyResult'] = _MUTATEBIDDINGSTRATEGYRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetBiddingStrategyRequest = _reflection.GeneratedProtocolMessageType('GetBiddingStrategyRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETBIDDINGSTRATEGYREQUEST,
  __module__ = 'google.ads.googleads_v0.proto.services.bidding_strategy_service_pb2'
  ,
  __doc__ = """Request message for
  [BiddingStrategyService.GetBiddingStrategy][google.ads.googleads.v0.services.BiddingStrategyService.GetBiddingStrategy].
  
  
  Attributes:
      resource_name:
          The resource name of the bidding strategy to fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.services.GetBiddingStrategyRequest)
  ))
_sym_db.RegisterMessage(GetBiddingStrategyRequest)

MutateBiddingStrategiesRequest = _reflection.GeneratedProtocolMessageType('MutateBiddingStrategiesRequest', (_message.Message,), dict(
  DESCRIPTOR = _MUTATEBIDDINGSTRATEGIESREQUEST,
  __module__ = 'google.ads.googleads_v0.proto.services.bidding_strategy_service_pb2'
  ,
  __doc__ = """Request message for
  [BiddingStrategyService.MutateBiddingStrategies][google.ads.googleads.v0.services.BiddingStrategyService.MutateBiddingStrategies].
  
  
  Attributes:
      customer_id:
          The ID of the customer whose bidding strategies are being
          modified.
      operations:
          The list of operations to perform on individual bidding
          strategies.
      partial_failure:
          If true, successful operations will be carried out and invalid
          operations will return errors. If false, all operations will
          be carried out in one transaction if and only if they are all
          valid. Default is false.
      validate_only:
          If true, the request is validated but not executed. Only
          errors are returned, not results.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.services.MutateBiddingStrategiesRequest)
  ))
_sym_db.RegisterMessage(MutateBiddingStrategiesRequest)

BiddingStrategyOperation = _reflection.GeneratedProtocolMessageType('BiddingStrategyOperation', (_message.Message,), dict(
  DESCRIPTOR = _BIDDINGSTRATEGYOPERATION,
  __module__ = 'google.ads.googleads_v0.proto.services.bidding_strategy_service_pb2'
  ,
  __doc__ = """A single operation (create, update, remove) on a bidding strategy.
  
  
  Attributes:
      update_mask:
          FieldMask that determines which resource fields are modified
          in an update.
      operation:
          The mutate operation.
      create:
          Create operation: No resource name is expected for the new
          bidding strategy.
      update:
          Update operation: The bidding strategy is expected to have a
          valid resource name.
      remove:
          Remove operation: A resource name for the removed bidding
          strategy is expected, in this format:  ``customers/{customer_i
          d}/biddingStrategies/{bidding_strategy_id}``
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.services.BiddingStrategyOperation)
  ))
_sym_db.RegisterMessage(BiddingStrategyOperation)

MutateBiddingStrategiesResponse = _reflection.GeneratedProtocolMessageType('MutateBiddingStrategiesResponse', (_message.Message,), dict(
  DESCRIPTOR = _MUTATEBIDDINGSTRATEGIESRESPONSE,
  __module__ = 'google.ads.googleads_v0.proto.services.bidding_strategy_service_pb2'
  ,
  __doc__ = """Response message for bidding strategy mutate.
  
  
  Attributes:
      partial_failure_error:
          Errors that pertain to operation failures in the partial
          failure mode. Returned only when partial\_failure = true and
          all errors occur inside the operations. If any errors occur
          outside the operations (e.g. auth errors), we return an RPC
          level error.
      results:
          All results for the mutate.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.services.MutateBiddingStrategiesResponse)
  ))
_sym_db.RegisterMessage(MutateBiddingStrategiesResponse)

MutateBiddingStrategyResult = _reflection.GeneratedProtocolMessageType('MutateBiddingStrategyResult', (_message.Message,), dict(
  DESCRIPTOR = _MUTATEBIDDINGSTRATEGYRESULT,
  __module__ = 'google.ads.googleads_v0.proto.services.bidding_strategy_service_pb2'
  ,
  __doc__ = """The result for the bidding strategy mutate.
  
  
  Attributes:
      resource_name:
          Returned for successful operations.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.services.MutateBiddingStrategyResult)
  ))
_sym_db.RegisterMessage(MutateBiddingStrategyResult)


DESCRIPTOR._options = None

_BIDDINGSTRATEGYSERVICE = _descriptor.ServiceDescriptor(
  name='BiddingStrategyService',
  full_name='google.ads.googleads.v0.services.BiddingStrategyService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=999,
  serialized_end=1448,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetBiddingStrategy',
    full_name='google.ads.googleads.v0.services.BiddingStrategyService.GetBiddingStrategy',
    index=0,
    containing_service=None,
    input_type=_GETBIDDINGSTRATEGYREQUEST,
    output_type=google_dot_ads_dot_googleads__v0_dot_proto_dot_resources_dot_bidding__strategy__pb2._BIDDINGSTRATEGY,
    serialized_options=_b('\202\323\344\223\0025\0223/v0/{resource_name=customers/*/biddingStrategies/*}'),
  ),
  _descriptor.MethodDescriptor(
    name='MutateBiddingStrategies',
    full_name='google.ads.googleads.v0.services.BiddingStrategyService.MutateBiddingStrategies',
    index=1,
    containing_service=None,
    input_type=_MUTATEBIDDINGSTRATEGIESREQUEST,
    output_type=_MUTATEBIDDINGSTRATEGIESRESPONSE,
    serialized_options=_b('\202\323\344\223\002;\"6/v0/customers/{customer_id=*}/biddingStrategies:mutate:\001*'),
  ),
])
_sym_db.RegisterServiceDescriptor(_BIDDINGSTRATEGYSERVICE)

DESCRIPTOR.services_by_name['BiddingStrategyService'] = _BIDDINGSTRATEGYSERVICE

# @@protoc_insertion_point(module_scope)
