# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.ads.google_ads.v1.proto.resources import account_budget_proposal_pb2 as google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_account__budget__proposal__pb2
from google.ads.google_ads.v1.proto.services import account_budget_proposal_service_pb2 as google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_account__budget__proposal__service__pb2


class AccountBudgetProposalServiceStub(object):
  """A service for managing account-level budgets via proposals.

  A proposal is a request to create a new budget or make changes to an
  existing one.

  Reads for account-level budgets managed by these proposals will be
  supported in a future version.  Please use BudgetOrderService until then:
  https://developers.google.com/adwords/api/docs/guides/budget-order

  Mutates:
  The CREATE operation creates a new proposal.
  UPDATE operations aren't supported.
  The REMOVE operation cancels a pending proposal.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetAccountBudgetProposal = channel.unary_unary(
        '/google.ads.googleads.v1.services.AccountBudgetProposalService/GetAccountBudgetProposal',
        request_serializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_account__budget__proposal__service__pb2.GetAccountBudgetProposalRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_account__budget__proposal__pb2.AccountBudgetProposal.FromString,
        )
    self.MutateAccountBudgetProposal = channel.unary_unary(
        '/google.ads.googleads.v1.services.AccountBudgetProposalService/MutateAccountBudgetProposal',
        request_serializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_account__budget__proposal__service__pb2.MutateAccountBudgetProposalRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_account__budget__proposal__service__pb2.MutateAccountBudgetProposalResponse.FromString,
        )


class AccountBudgetProposalServiceServicer(object):
  """A service for managing account-level budgets via proposals.

  A proposal is a request to create a new budget or make changes to an
  existing one.

  Reads for account-level budgets managed by these proposals will be
  supported in a future version.  Please use BudgetOrderService until then:
  https://developers.google.com/adwords/api/docs/guides/budget-order

  Mutates:
  The CREATE operation creates a new proposal.
  UPDATE operations aren't supported.
  The REMOVE operation cancels a pending proposal.
  """

  def GetAccountBudgetProposal(self, request, context):
    """Returns an account-level budget proposal in full detail.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def MutateAccountBudgetProposal(self, request, context):
    """Creates, updates, or removes account budget proposals.  Operation statuses
    are returned.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_AccountBudgetProposalServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetAccountBudgetProposal': grpc.unary_unary_rpc_method_handler(
          servicer.GetAccountBudgetProposal,
          request_deserializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_account__budget__proposal__service__pb2.GetAccountBudgetProposalRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_account__budget__proposal__pb2.AccountBudgetProposal.SerializeToString,
      ),
      'MutateAccountBudgetProposal': grpc.unary_unary_rpc_method_handler(
          servicer.MutateAccountBudgetProposal,
          request_deserializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_account__budget__proposal__service__pb2.MutateAccountBudgetProposalRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_account__budget__proposal__service__pb2.MutateAccountBudgetProposalResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.ads.googleads.v1.services.AccountBudgetProposalService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
