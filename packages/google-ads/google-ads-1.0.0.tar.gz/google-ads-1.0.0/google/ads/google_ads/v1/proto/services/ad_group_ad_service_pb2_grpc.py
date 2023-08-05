# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.ads.google_ads.v1.proto.resources import ad_group_ad_pb2 as google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_ad__group__ad__pb2
from google.ads.google_ads.v1.proto.services import ad_group_ad_service_pb2 as google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_ad__group__ad__service__pb2


class AdGroupAdServiceStub(object):
  """Service to manage ads in an ad group.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetAdGroupAd = channel.unary_unary(
        '/google.ads.googleads.v1.services.AdGroupAdService/GetAdGroupAd',
        request_serializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_ad__group__ad__service__pb2.GetAdGroupAdRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_ad__group__ad__pb2.AdGroupAd.FromString,
        )
    self.MutateAdGroupAds = channel.unary_unary(
        '/google.ads.googleads.v1.services.AdGroupAdService/MutateAdGroupAds',
        request_serializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_ad__group__ad__service__pb2.MutateAdGroupAdsRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_ad__group__ad__service__pb2.MutateAdGroupAdsResponse.FromString,
        )


class AdGroupAdServiceServicer(object):
  """Service to manage ads in an ad group.
  """

  def GetAdGroupAd(self, request, context):
    """Returns the requested ad in full detail.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def MutateAdGroupAds(self, request, context):
    """Creates, updates, or removes ads. Operation statuses are returned.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_AdGroupAdServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetAdGroupAd': grpc.unary_unary_rpc_method_handler(
          servicer.GetAdGroupAd,
          request_deserializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_ad__group__ad__service__pb2.GetAdGroupAdRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_ad__group__ad__pb2.AdGroupAd.SerializeToString,
      ),
      'MutateAdGroupAds': grpc.unary_unary_rpc_method_handler(
          servicer.MutateAdGroupAds,
          request_deserializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_ad__group__ad__service__pb2.MutateAdGroupAdsRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_ad__group__ad__service__pb2.MutateAdGroupAdsResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.ads.googleads.v1.services.AdGroupAdService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
