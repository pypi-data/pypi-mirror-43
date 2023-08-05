# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.ads.google_ads.v1.proto.resources import language_constant_pb2 as google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_language__constant__pb2
from google.ads.google_ads.v1.proto.services import language_constant_service_pb2 as google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_language__constant__service__pb2


class LanguageConstantServiceStub(object):
  """Service to fetch language constants.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetLanguageConstant = channel.unary_unary(
        '/google.ads.googleads.v1.services.LanguageConstantService/GetLanguageConstant',
        request_serializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_language__constant__service__pb2.GetLanguageConstantRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_language__constant__pb2.LanguageConstant.FromString,
        )


class LanguageConstantServiceServicer(object):
  """Service to fetch language constants.
  """

  def GetLanguageConstant(self, request, context):
    """Returns the requested language constant.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_LanguageConstantServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetLanguageConstant': grpc.unary_unary_rpc_method_handler(
          servicer.GetLanguageConstant,
          request_deserializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_language__constant__service__pb2.GetLanguageConstantRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_language__constant__pb2.LanguageConstant.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.ads.googleads.v1.services.LanguageConstantService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
