# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.ads.google_ads.v0.proto.resources import operating_system_version_constant_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_resources_dot_operating__system__version__constant__pb2
from google.ads.google_ads.v0.proto.services import operating_system_version_constant_service_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_services_dot_operating__system__version__constant__service__pb2


class OperatingSystemVersionConstantServiceStub(object):
  """Service to fetch Operating System Version constants.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetOperatingSystemVersionConstant = channel.unary_unary(
        '/google.ads.googleads.v0.services.OperatingSystemVersionConstantService/GetOperatingSystemVersionConstant',
        request_serializer=google_dot_ads_dot_googleads__v0_dot_proto_dot_services_dot_operating__system__version__constant__service__pb2.GetOperatingSystemVersionConstantRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v0_dot_proto_dot_resources_dot_operating__system__version__constant__pb2.OperatingSystemVersionConstant.FromString,
        )


class OperatingSystemVersionConstantServiceServicer(object):
  """Service to fetch Operating System Version constants.
  """

  def GetOperatingSystemVersionConstant(self, request, context):
    """Returns the requested OS version constant in full detail.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_OperatingSystemVersionConstantServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetOperatingSystemVersionConstant': grpc.unary_unary_rpc_method_handler(
          servicer.GetOperatingSystemVersionConstant,
          request_deserializer=google_dot_ads_dot_googleads__v0_dot_proto_dot_services_dot_operating__system__version__constant__service__pb2.GetOperatingSystemVersionConstantRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v0_dot_proto_dot_resources_dot_operating__system__version__constant__pb2.OperatingSystemVersionConstant.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.ads.googleads.v0.services.OperatingSystemVersionConstantService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
