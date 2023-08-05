# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/resources/mutate_job.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v1.proto.enums import mutate_job_status_pb2 as google_dot_ads_dot_googleads__v1_dot_proto_dot_enums_dot_mutate__job__status__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v1/proto/resources/mutate_job.proto',
  package='google.ads.googleads.v1.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v1.resourcesB\016MutateJobProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v1/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V1.Resources\312\002!Google\\Ads\\GoogleAds\\V1\\Resources\352\002%Google::Ads::GoogleAds::V1::Resources'),
  serialized_pb=_b('\n8google/ads/googleads_v1/proto/resources/mutate_job.proto\x12!google.ads.googleads.v1.resources\x1a;google/ads/googleads_v1/proto/enums/mutate_job_status.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/api/annotations.proto\"\xfe\x03\n\tMutateJob\x12\x15\n\rresource_name\x18\x01 \x01(\t\x12\'\n\x02id\x18\x02 \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12=\n\x17next_add_sequence_token\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12P\n\x08metadata\x18\x04 \x01(\x0b\x32>.google.ads.googleads.v1.resources.MutateJob.MutateJobMetadata\x12R\n\x06status\x18\x05 \x01(\x0e\x32\x42.google.ads.googleads.v1.enums.MutateJobStatusEnum.MutateJobStatus\x1a\xcb\x01\n\x11MutateJobMetadata\x12\x38\n\x12\x63reation_date_time\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12:\n\x14\x63ompletion_date_time\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12@\n\x1a\x65stimated_completion_ratio\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.DoubleValueB\xfb\x01\n%com.google.ads.googleads.v1.resourcesB\x0eMutateJobProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v1/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V1.Resources\xca\x02!Google\\Ads\\GoogleAds\\V1\\Resources\xea\x02%Google::Ads::GoogleAds::V1::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v1_dot_proto_dot_enums_dot_mutate__job__status__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_MUTATEJOB_MUTATEJOBMETADATA = _descriptor.Descriptor(
  name='MutateJobMetadata',
  full_name='google.ads.googleads.v1.resources.MutateJob.MutateJobMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='creation_date_time', full_name='google.ads.googleads.v1.resources.MutateJob.MutateJobMetadata.creation_date_time', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='completion_date_time', full_name='google.ads.googleads.v1.resources.MutateJob.MutateJobMetadata.completion_date_time', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='estimated_completion_ratio', full_name='google.ads.googleads.v1.resources.MutateJob.MutateJobMetadata.estimated_completion_ratio', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=526,
  serialized_end=729,
)

_MUTATEJOB = _descriptor.Descriptor(
  name='MutateJob',
  full_name='google.ads.googleads.v1.resources.MutateJob',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v1.resources.MutateJob.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='google.ads.googleads.v1.resources.MutateJob.id', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='next_add_sequence_token', full_name='google.ads.googleads.v1.resources.MutateJob.next_add_sequence_token', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='metadata', full_name='google.ads.googleads.v1.resources.MutateJob.metadata', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='google.ads.googleads.v1.resources.MutateJob.status', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_MUTATEJOB_MUTATEJOBMETADATA, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=219,
  serialized_end=729,
)

_MUTATEJOB_MUTATEJOBMETADATA.fields_by_name['creation_date_time'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_MUTATEJOB_MUTATEJOBMETADATA.fields_by_name['completion_date_time'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_MUTATEJOB_MUTATEJOBMETADATA.fields_by_name['estimated_completion_ratio'].message_type = google_dot_protobuf_dot_wrappers__pb2._DOUBLEVALUE
_MUTATEJOB_MUTATEJOBMETADATA.containing_type = _MUTATEJOB
_MUTATEJOB.fields_by_name['id'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_MUTATEJOB.fields_by_name['next_add_sequence_token'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_MUTATEJOB.fields_by_name['metadata'].message_type = _MUTATEJOB_MUTATEJOBMETADATA
_MUTATEJOB.fields_by_name['status'].enum_type = google_dot_ads_dot_googleads__v1_dot_proto_dot_enums_dot_mutate__job__status__pb2._MUTATEJOBSTATUSENUM_MUTATEJOBSTATUS
DESCRIPTOR.message_types_by_name['MutateJob'] = _MUTATEJOB
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MutateJob = _reflection.GeneratedProtocolMessageType('MutateJob', (_message.Message,), dict(

  MutateJobMetadata = _reflection.GeneratedProtocolMessageType('MutateJobMetadata', (_message.Message,), dict(
    DESCRIPTOR = _MUTATEJOB_MUTATEJOBMETADATA,
    __module__ = 'google.ads.googleads_v1.proto.resources.mutate_job_pb2'
    ,
    __doc__ = """Additional information about the mutate job. This message is also used
    as metadata returned in mutate job Long Running Operations.
    
    
    Attributes:
        creation_date_time:
            The time when this mutate job was created. Formatted as yyyy-
            mm-dd hh:mm:ss. Example: "2018-03-05 09:15:00"
        completion_date_time:
            The time when this mutate job was completed. Formatted as
            yyyy-MM-dd HH:mm:ss. Example: "2018-03-05 09:16:00"
        estimated_completion_ratio:
            The fraction (between 0.0 and 1.0) of mutates that have been
            processed. This is empty if the job hasn't started running
            yet.
    """,
    # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.resources.MutateJob.MutateJobMetadata)
    ))
  ,
  DESCRIPTOR = _MUTATEJOB,
  __module__ = 'google.ads.googleads_v1.proto.resources.mutate_job_pb2'
  ,
  __doc__ = """A list of mutates being processed asynchronously. The mutates are
  uploaded by the user. The mutates themselves aren’t readable and the
  results of the job can only be read using
  MutateJobService.ListMutateJobResults.
  
  
  Attributes:
      resource_name:
          The resource name of the mutate job. Mutate job resource names
          have the form:
          ``customers/{customer_id}/mutateJobs/{mutate_job_id}``
      id:
          ID of this mutate job.
      next_add_sequence_token:
          The next sequence token to use when adding operations. Only
          set when the mutate job status is PENDING.
      metadata:
          Contains additional information about this mutate job.
      status:
          Status of this mutate job.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.resources.MutateJob)
  ))
_sym_db.RegisterMessage(MutateJob)
_sym_db.RegisterMessage(MutateJob.MutateJobMetadata)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
