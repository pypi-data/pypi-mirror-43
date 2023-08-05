# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/services/account_budget_proposal_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v0.proto.resources import account_budget_proposal_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_resources_dot_account__budget__proposal__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/services/account_budget_proposal_service.proto',
  package='google.ads.googleads.v0.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v0.servicesB!AccountBudgetProposalServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v0/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V0.Services\312\002 Google\\Ads\\GoogleAds\\V0\\Services\352\002$Google::Ads::GoogleAds::V0::Services'),
  serialized_pb=_b('\nLgoogle/ads/googleads_v0/proto/services/account_budget_proposal_service.proto\x12 google.ads.googleads.v0.services\x1a\x45google/ads/googleads_v0/proto/resources/account_budget_proposal.proto\x1a\x1cgoogle/api/annotations.proto\x1a google/protobuf/field_mask.proto\"8\n\x1fGetAccountBudgetProposalRequest\x12\x15\n\rresource_name\x18\x01 \x01(\t\"\x8e\x01\n\"MutateAccountBudgetProposalRequest\x12\x13\n\x0b\x63ustomer_id\x18\x01 \x01(\t\x12S\n\toperation\x18\x02 \x01(\x0b\x32@.google.ads.googleads.v0.services.AccountBudgetProposalOperation\"\xbc\x01\n\x1e\x41\x63\x63ountBudgetProposalOperation\x12/\n\x0bupdate_mask\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12J\n\x06\x63reate\x18\x02 \x01(\x0b\x32\x38.google.ads.googleads.v0.resources.AccountBudgetProposalH\x00\x12\x10\n\x06remove\x18\x01 \x01(\tH\x00\x42\x0b\n\toperation\"z\n#MutateAccountBudgetProposalResponse\x12S\n\x06result\x18\x02 \x01(\x0b\x32\x43.google.ads.googleads.v0.services.MutateAccountBudgetProposalResult\":\n!MutateAccountBudgetProposalResult\x12\x15\n\rresource_name\x18\x01 \x01(\t2\xef\x03\n\x1c\x41\x63\x63ountBudgetProposalService\x12\xd9\x01\n\x18GetAccountBudgetProposal\x12\x41.google.ads.googleads.v0.services.GetAccountBudgetProposalRequest\x1a\x38.google.ads.googleads.v0.resources.AccountBudgetProposal\"@\x82\xd3\xe4\x93\x02:\x12\x38/v0/{resource_name=customers/*/accountBudgetProposals/*}\x12\xf2\x01\n\x1bMutateAccountBudgetProposal\x12\x44.google.ads.googleads.v0.services.MutateAccountBudgetProposalRequest\x1a\x45.google.ads.googleads.v0.services.MutateAccountBudgetProposalResponse\"F\x82\xd3\xe4\x93\x02@\";/v0/customers/{customer_id=*}/accountBudgetProposals:mutate:\x01*B\x88\x02\n$com.google.ads.googleads.v0.servicesB!AccountBudgetProposalServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v0/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V0.Services\xca\x02 Google\\Ads\\GoogleAds\\V0\\Services\xea\x02$Google::Ads::GoogleAds::V0::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v0_dot_proto_dot_resources_dot_account__budget__proposal__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_protobuf_dot_field__mask__pb2.DESCRIPTOR,])




_GETACCOUNTBUDGETPROPOSALREQUEST = _descriptor.Descriptor(
  name='GetAccountBudgetProposalRequest',
  full_name='google.ads.googleads.v0.services.GetAccountBudgetProposalRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v0.services.GetAccountBudgetProposalRequest.resource_name', index=0,
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
  serialized_start=249,
  serialized_end=305,
)


_MUTATEACCOUNTBUDGETPROPOSALREQUEST = _descriptor.Descriptor(
  name='MutateAccountBudgetProposalRequest',
  full_name='google.ads.googleads.v0.services.MutateAccountBudgetProposalRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='customer_id', full_name='google.ads.googleads.v0.services.MutateAccountBudgetProposalRequest.customer_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='operation', full_name='google.ads.googleads.v0.services.MutateAccountBudgetProposalRequest.operation', index=1,
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
  serialized_start=308,
  serialized_end=450,
)


_ACCOUNTBUDGETPROPOSALOPERATION = _descriptor.Descriptor(
  name='AccountBudgetProposalOperation',
  full_name='google.ads.googleads.v0.services.AccountBudgetProposalOperation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='update_mask', full_name='google.ads.googleads.v0.services.AccountBudgetProposalOperation.update_mask', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='create', full_name='google.ads.googleads.v0.services.AccountBudgetProposalOperation.create', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='remove', full_name='google.ads.googleads.v0.services.AccountBudgetProposalOperation.remove', index=2,
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
    _descriptor.OneofDescriptor(
      name='operation', full_name='google.ads.googleads.v0.services.AccountBudgetProposalOperation.operation',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=453,
  serialized_end=641,
)


_MUTATEACCOUNTBUDGETPROPOSALRESPONSE = _descriptor.Descriptor(
  name='MutateAccountBudgetProposalResponse',
  full_name='google.ads.googleads.v0.services.MutateAccountBudgetProposalResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='google.ads.googleads.v0.services.MutateAccountBudgetProposalResponse.result', index=0,
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
  serialized_start=643,
  serialized_end=765,
)


_MUTATEACCOUNTBUDGETPROPOSALRESULT = _descriptor.Descriptor(
  name='MutateAccountBudgetProposalResult',
  full_name='google.ads.googleads.v0.services.MutateAccountBudgetProposalResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v0.services.MutateAccountBudgetProposalResult.resource_name', index=0,
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
  serialized_start=767,
  serialized_end=825,
)

_MUTATEACCOUNTBUDGETPROPOSALREQUEST.fields_by_name['operation'].message_type = _ACCOUNTBUDGETPROPOSALOPERATION
_ACCOUNTBUDGETPROPOSALOPERATION.fields_by_name['update_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_ACCOUNTBUDGETPROPOSALOPERATION.fields_by_name['create'].message_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_resources_dot_account__budget__proposal__pb2._ACCOUNTBUDGETPROPOSAL
_ACCOUNTBUDGETPROPOSALOPERATION.oneofs_by_name['operation'].fields.append(
  _ACCOUNTBUDGETPROPOSALOPERATION.fields_by_name['create'])
_ACCOUNTBUDGETPROPOSALOPERATION.fields_by_name['create'].containing_oneof = _ACCOUNTBUDGETPROPOSALOPERATION.oneofs_by_name['operation']
_ACCOUNTBUDGETPROPOSALOPERATION.oneofs_by_name['operation'].fields.append(
  _ACCOUNTBUDGETPROPOSALOPERATION.fields_by_name['remove'])
_ACCOUNTBUDGETPROPOSALOPERATION.fields_by_name['remove'].containing_oneof = _ACCOUNTBUDGETPROPOSALOPERATION.oneofs_by_name['operation']
_MUTATEACCOUNTBUDGETPROPOSALRESPONSE.fields_by_name['result'].message_type = _MUTATEACCOUNTBUDGETPROPOSALRESULT
DESCRIPTOR.message_types_by_name['GetAccountBudgetProposalRequest'] = _GETACCOUNTBUDGETPROPOSALREQUEST
DESCRIPTOR.message_types_by_name['MutateAccountBudgetProposalRequest'] = _MUTATEACCOUNTBUDGETPROPOSALREQUEST
DESCRIPTOR.message_types_by_name['AccountBudgetProposalOperation'] = _ACCOUNTBUDGETPROPOSALOPERATION
DESCRIPTOR.message_types_by_name['MutateAccountBudgetProposalResponse'] = _MUTATEACCOUNTBUDGETPROPOSALRESPONSE
DESCRIPTOR.message_types_by_name['MutateAccountBudgetProposalResult'] = _MUTATEACCOUNTBUDGETPROPOSALRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetAccountBudgetProposalRequest = _reflection.GeneratedProtocolMessageType('GetAccountBudgetProposalRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETACCOUNTBUDGETPROPOSALREQUEST,
  __module__ = 'google.ads.googleads_v0.proto.services.account_budget_proposal_service_pb2'
  ,
  __doc__ = """Request message for
  [AccountBudgetProposalService.GetAccountBudgetProposal][google.ads.googleads.v0.services.AccountBudgetProposalService.GetAccountBudgetProposal].
  
  
  Attributes:
      resource_name:
          The resource name of the account-level budget proposal to
          fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.services.GetAccountBudgetProposalRequest)
  ))
_sym_db.RegisterMessage(GetAccountBudgetProposalRequest)

MutateAccountBudgetProposalRequest = _reflection.GeneratedProtocolMessageType('MutateAccountBudgetProposalRequest', (_message.Message,), dict(
  DESCRIPTOR = _MUTATEACCOUNTBUDGETPROPOSALREQUEST,
  __module__ = 'google.ads.googleads_v0.proto.services.account_budget_proposal_service_pb2'
  ,
  __doc__ = """Request message for
  [AccountBudgetProposalService.MutateAccountBudgetProposal][google.ads.googleads.v0.services.AccountBudgetProposalService.MutateAccountBudgetProposal].
  
  
  Attributes:
      customer_id:
          The ID of the customer.
      operation:
          The operation to perform on an individual account-level budget
          proposal.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.services.MutateAccountBudgetProposalRequest)
  ))
_sym_db.RegisterMessage(MutateAccountBudgetProposalRequest)

AccountBudgetProposalOperation = _reflection.GeneratedProtocolMessageType('AccountBudgetProposalOperation', (_message.Message,), dict(
  DESCRIPTOR = _ACCOUNTBUDGETPROPOSALOPERATION,
  __module__ = 'google.ads.googleads_v0.proto.services.account_budget_proposal_service_pb2'
  ,
  __doc__ = """A single operation to propose the creation of a new account-level budget
  or edit/end/remove an existing one.
  
  
  Attributes:
      update_mask:
          FieldMask that determines which budget fields are modified.
          While budgets may be modified, proposals that propose such
          modifications are final. Therefore, update operations are not
          supported for proposals.  Proposals that modify budgets have
          the 'update' proposal type. Specifying a mask for any other
          proposal type is considered an error.
      operation:
          The mutate operation.
      create:
          Create operation: A new proposal to create a new budget, edit
          an existing budget, end an actively running budget, or remove
          an approved budget scheduled to start in the future. No
          resource name is expected for the new proposal.
      remove:
          Remove operation: A resource name for the removed proposal is
          expected, in this format:  ``customers/{customer_id}/accountBu
          dgetProposals/{account_budget_proposal_id}`` A request may be
          cancelled iff it is pending.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.services.AccountBudgetProposalOperation)
  ))
_sym_db.RegisterMessage(AccountBudgetProposalOperation)

MutateAccountBudgetProposalResponse = _reflection.GeneratedProtocolMessageType('MutateAccountBudgetProposalResponse', (_message.Message,), dict(
  DESCRIPTOR = _MUTATEACCOUNTBUDGETPROPOSALRESPONSE,
  __module__ = 'google.ads.googleads_v0.proto.services.account_budget_proposal_service_pb2'
  ,
  __doc__ = """Response message for account-level budget mutate operations.
  
  
  Attributes:
      result:
          The result of the mutate.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.services.MutateAccountBudgetProposalResponse)
  ))
_sym_db.RegisterMessage(MutateAccountBudgetProposalResponse)

MutateAccountBudgetProposalResult = _reflection.GeneratedProtocolMessageType('MutateAccountBudgetProposalResult', (_message.Message,), dict(
  DESCRIPTOR = _MUTATEACCOUNTBUDGETPROPOSALRESULT,
  __module__ = 'google.ads.googleads_v0.proto.services.account_budget_proposal_service_pb2'
  ,
  __doc__ = """The result for the account budget proposal mutate.
  
  
  Attributes:
      resource_name:
          Returned for successful operations.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.services.MutateAccountBudgetProposalResult)
  ))
_sym_db.RegisterMessage(MutateAccountBudgetProposalResult)


DESCRIPTOR._options = None

_ACCOUNTBUDGETPROPOSALSERVICE = _descriptor.ServiceDescriptor(
  name='AccountBudgetProposalService',
  full_name='google.ads.googleads.v0.services.AccountBudgetProposalService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=828,
  serialized_end=1323,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetAccountBudgetProposal',
    full_name='google.ads.googleads.v0.services.AccountBudgetProposalService.GetAccountBudgetProposal',
    index=0,
    containing_service=None,
    input_type=_GETACCOUNTBUDGETPROPOSALREQUEST,
    output_type=google_dot_ads_dot_googleads__v0_dot_proto_dot_resources_dot_account__budget__proposal__pb2._ACCOUNTBUDGETPROPOSAL,
    serialized_options=_b('\202\323\344\223\002:\0228/v0/{resource_name=customers/*/accountBudgetProposals/*}'),
  ),
  _descriptor.MethodDescriptor(
    name='MutateAccountBudgetProposal',
    full_name='google.ads.googleads.v0.services.AccountBudgetProposalService.MutateAccountBudgetProposal',
    index=1,
    containing_service=None,
    input_type=_MUTATEACCOUNTBUDGETPROPOSALREQUEST,
    output_type=_MUTATEACCOUNTBUDGETPROPOSALRESPONSE,
    serialized_options=_b('\202\323\344\223\002@\";/v0/customers/{customer_id=*}/accountBudgetProposals:mutate:\001*'),
  ),
])
_sym_db.RegisterServiceDescriptor(_ACCOUNTBUDGETPROPOSALSERVICE)

DESCRIPTOR.services_by_name['AccountBudgetProposalService'] = _ACCOUNTBUDGETPROPOSALSERVICE

# @@protoc_insertion_point(module_scope)
