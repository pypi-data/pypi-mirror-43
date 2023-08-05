# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v0/proto/services/payments_account_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v0.proto.resources import payments_account_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_resources_dot_payments__account__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v0/proto/services/payments_account_service.proto',
  package='google.ads.googleads.v0.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v0.servicesB\033PaymentsAccountServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v0/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V0.Services\312\002 Google\\Ads\\GoogleAds\\V0\\Services\352\002$Google::Ads::GoogleAds::V0::Services'),
  serialized_pb=_b('\nEgoogle/ads/googleads_v0/proto/services/payments_account_service.proto\x12 google.ads.googleads.v0.services\x1a>google/ads/googleads_v0/proto/resources/payments_account.proto\x1a\x1cgoogle/api/annotations.proto\"2\n\x1bListPaymentsAccountsRequest\x12\x13\n\x0b\x63ustomer_id\x18\x01 \x01(\t\"m\n\x1cListPaymentsAccountsResponse\x12M\n\x11payments_accounts\x18\x01 \x03(\x0b\x32\x32.google.ads.googleads.v0.resources.PaymentsAccount2\xe8\x01\n\x16PaymentsAccountService\x12\xcd\x01\n\x14ListPaymentsAccounts\x12=.google.ads.googleads.v0.services.ListPaymentsAccountsRequest\x1a>.google.ads.googleads.v0.services.ListPaymentsAccountsResponse\"6\x82\xd3\xe4\x93\x02\x30\x12./v0/customers/{customer_id=*}/paymentsAccountsB\x82\x02\n$com.google.ads.googleads.v0.servicesB\x1bPaymentsAccountServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v0/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V0.Services\xca\x02 Google\\Ads\\GoogleAds\\V0\\Services\xea\x02$Google::Ads::GoogleAds::V0::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v0_dot_proto_dot_resources_dot_payments__account__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_LISTPAYMENTSACCOUNTSREQUEST = _descriptor.Descriptor(
  name='ListPaymentsAccountsRequest',
  full_name='google.ads.googleads.v0.services.ListPaymentsAccountsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='customer_id', full_name='google.ads.googleads.v0.services.ListPaymentsAccountsRequest.customer_id', index=0,
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
  serialized_start=201,
  serialized_end=251,
)


_LISTPAYMENTSACCOUNTSRESPONSE = _descriptor.Descriptor(
  name='ListPaymentsAccountsResponse',
  full_name='google.ads.googleads.v0.services.ListPaymentsAccountsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='payments_accounts', full_name='google.ads.googleads.v0.services.ListPaymentsAccountsResponse.payments_accounts', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=253,
  serialized_end=362,
)

_LISTPAYMENTSACCOUNTSRESPONSE.fields_by_name['payments_accounts'].message_type = google_dot_ads_dot_googleads__v0_dot_proto_dot_resources_dot_payments__account__pb2._PAYMENTSACCOUNT
DESCRIPTOR.message_types_by_name['ListPaymentsAccountsRequest'] = _LISTPAYMENTSACCOUNTSREQUEST
DESCRIPTOR.message_types_by_name['ListPaymentsAccountsResponse'] = _LISTPAYMENTSACCOUNTSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ListPaymentsAccountsRequest = _reflection.GeneratedProtocolMessageType('ListPaymentsAccountsRequest', (_message.Message,), dict(
  DESCRIPTOR = _LISTPAYMENTSACCOUNTSREQUEST,
  __module__ = 'google.ads.googleads_v0.proto.services.payments_account_service_pb2'
  ,
  __doc__ = """Request message for fetching all accessible Payments accounts.
  
  
  Attributes:
      customer_id:
          The ID of the customer to apply the PaymentsAccount list
          operation to.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.services.ListPaymentsAccountsRequest)
  ))
_sym_db.RegisterMessage(ListPaymentsAccountsRequest)

ListPaymentsAccountsResponse = _reflection.GeneratedProtocolMessageType('ListPaymentsAccountsResponse', (_message.Message,), dict(
  DESCRIPTOR = _LISTPAYMENTSACCOUNTSRESPONSE,
  __module__ = 'google.ads.googleads_v0.proto.services.payments_account_service_pb2'
  ,
  __doc__ = """Response message for
  [PaymentsAccountService.ListPaymentsAccounts][google.ads.googleads.v0.services.PaymentsAccountService.ListPaymentsAccounts].
  
  
  Attributes:
      payments_accounts:
          The list of accessible Payments accounts.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v0.services.ListPaymentsAccountsResponse)
  ))
_sym_db.RegisterMessage(ListPaymentsAccountsResponse)


DESCRIPTOR._options = None

_PAYMENTSACCOUNTSERVICE = _descriptor.ServiceDescriptor(
  name='PaymentsAccountService',
  full_name='google.ads.googleads.v0.services.PaymentsAccountService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=365,
  serialized_end=597,
  methods=[
  _descriptor.MethodDescriptor(
    name='ListPaymentsAccounts',
    full_name='google.ads.googleads.v0.services.PaymentsAccountService.ListPaymentsAccounts',
    index=0,
    containing_service=None,
    input_type=_LISTPAYMENTSACCOUNTSREQUEST,
    output_type=_LISTPAYMENTSACCOUNTSRESPONSE,
    serialized_options=_b('\202\323\344\223\0020\022./v0/customers/{customer_id=*}/paymentsAccounts'),
  ),
])
_sym_db.RegisterServiceDescriptor(_PAYMENTSACCOUNTSERVICE)

DESCRIPTOR.services_by_name['PaymentsAccountService'] = _PAYMENTSACCOUNTSERVICE

# @@protoc_insertion_point(module_scope)
