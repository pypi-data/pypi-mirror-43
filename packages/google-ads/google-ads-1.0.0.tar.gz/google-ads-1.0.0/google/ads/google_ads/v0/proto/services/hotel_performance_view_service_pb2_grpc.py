# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.ads.google_ads.v0.proto.resources import hotel_performance_view_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_resources_dot_hotel__performance__view__pb2
from google.ads.google_ads.v0.proto.services import hotel_performance_view_service_pb2 as google_dot_ads_dot_googleads__v0_dot_proto_dot_services_dot_hotel__performance__view__service__pb2


class HotelPerformanceViewServiceStub(object):
  """Service to manage Hotel Performance Views.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetHotelPerformanceView = channel.unary_unary(
        '/google.ads.googleads.v0.services.HotelPerformanceViewService/GetHotelPerformanceView',
        request_serializer=google_dot_ads_dot_googleads__v0_dot_proto_dot_services_dot_hotel__performance__view__service__pb2.GetHotelPerformanceViewRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v0_dot_proto_dot_resources_dot_hotel__performance__view__pb2.HotelPerformanceView.FromString,
        )


class HotelPerformanceViewServiceServicer(object):
  """Service to manage Hotel Performance Views.
  """

  def GetHotelPerformanceView(self, request, context):
    """Returns the requested Hotel Performance View in full detail.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_HotelPerformanceViewServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetHotelPerformanceView': grpc.unary_unary_rpc_method_handler(
          servicer.GetHotelPerformanceView,
          request_deserializer=google_dot_ads_dot_googleads__v0_dot_proto_dot_services_dot_hotel__performance__view__service__pb2.GetHotelPerformanceViewRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v0_dot_proto_dot_resources_dot_hotel__performance__view__pb2.HotelPerformanceView.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.ads.googleads.v0.services.HotelPerformanceViewService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
