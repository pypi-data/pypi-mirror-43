# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from . import plugin_pb2 as plugin__pb2
from . import provider_pb2 as provider__pb2


class ResourceProviderStub(object):
  """ResourceProvider is a service that understands how to create, read, update, or delete resources for types defined
  within a single package.  It is driven by the overall planning engine in response to resource diffs.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.CheckConfig = channel.unary_unary(
        '/pulumirpc.ResourceProvider/CheckConfig',
        request_serializer=provider__pb2.CheckRequest.SerializeToString,
        response_deserializer=provider__pb2.CheckResponse.FromString,
        )
    self.DiffConfig = channel.unary_unary(
        '/pulumirpc.ResourceProvider/DiffConfig',
        request_serializer=provider__pb2.DiffRequest.SerializeToString,
        response_deserializer=provider__pb2.DiffResponse.FromString,
        )
    self.Configure = channel.unary_unary(
        '/pulumirpc.ResourceProvider/Configure',
        request_serializer=provider__pb2.ConfigureRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.Invoke = channel.unary_unary(
        '/pulumirpc.ResourceProvider/Invoke',
        request_serializer=provider__pb2.InvokeRequest.SerializeToString,
        response_deserializer=provider__pb2.InvokeResponse.FromString,
        )
    self.Check = channel.unary_unary(
        '/pulumirpc.ResourceProvider/Check',
        request_serializer=provider__pb2.CheckRequest.SerializeToString,
        response_deserializer=provider__pb2.CheckResponse.FromString,
        )
    self.Diff = channel.unary_unary(
        '/pulumirpc.ResourceProvider/Diff',
        request_serializer=provider__pb2.DiffRequest.SerializeToString,
        response_deserializer=provider__pb2.DiffResponse.FromString,
        )
    self.Create = channel.unary_unary(
        '/pulumirpc.ResourceProvider/Create',
        request_serializer=provider__pb2.CreateRequest.SerializeToString,
        response_deserializer=provider__pb2.CreateResponse.FromString,
        )
    self.Read = channel.unary_unary(
        '/pulumirpc.ResourceProvider/Read',
        request_serializer=provider__pb2.ReadRequest.SerializeToString,
        response_deserializer=provider__pb2.ReadResponse.FromString,
        )
    self.Update = channel.unary_unary(
        '/pulumirpc.ResourceProvider/Update',
        request_serializer=provider__pb2.UpdateRequest.SerializeToString,
        response_deserializer=provider__pb2.UpdateResponse.FromString,
        )
    self.Delete = channel.unary_unary(
        '/pulumirpc.ResourceProvider/Delete',
        request_serializer=provider__pb2.DeleteRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.Cancel = channel.unary_unary(
        '/pulumirpc.ResourceProvider/Cancel',
        request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.GetPluginInfo = channel.unary_unary(
        '/pulumirpc.ResourceProvider/GetPluginInfo',
        request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        response_deserializer=plugin__pb2.PluginInfo.FromString,
        )


class ResourceProviderServicer(object):
  """ResourceProvider is a service that understands how to create, read, update, or delete resources for types defined
  within a single package.  It is driven by the overall planning engine in response to resource diffs.
  """

  def CheckConfig(self, request, context):
    """CheckConfig validates the configuration for this resource provider.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DiffConfig(self, request, context):
    """DiffConfig checks the impact a hypothetical change to this provider's configuration will have on the provider.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Configure(self, request, context):
    """Configure configures the resource provider with "globals" that control its behavior.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Invoke(self, request, context):
    """Invoke dynamically executes a built-in function in the provider.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Check(self, request, context):
    """Check validates that the given property bag is valid for a resource of the given type and returns the inputs
    that should be passed to successive calls to Diff, Create, or Update for this resource. As a rule, the provider
    inputs returned by a call to Check should preserve the original representation of the properties as present in
    the program inputs. Though this rule is not required for correctness, violations thereof can negatively impact
    the end-user experience, as the provider inputs are using for detecting and rendering diffs.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Diff(self, request, context):
    """Diff checks what impacts a hypothetical update will have on the resource's properties.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Create(self, request, context):
    """Create allocates a new instance of the provided resource and returns its unique ID afterwards.  (The input ID
    must be blank.)  If this call fails, the resource must not have been created (i.e., it is "transacational").
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Read(self, request, context):
    """Read the current live state associated with a resource.  Enough state must be include in the inputs to uniquely
    identify the resource; this is typically just the resource ID, but may also include some properties.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Update(self, request, context):
    """Update updates an existing resource with new values.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Delete(self, request, context):
    """Delete tears down an existing resource with the given ID.  If it fails, the resource is assumed to still exist.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Cancel(self, request, context):
    """Cancel signals the provider to abort all outstanding resource operations.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetPluginInfo(self, request, context):
    """GetPluginInfo returns generic information about this plugin, like its version.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ResourceProviderServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'CheckConfig': grpc.unary_unary_rpc_method_handler(
          servicer.CheckConfig,
          request_deserializer=provider__pb2.CheckRequest.FromString,
          response_serializer=provider__pb2.CheckResponse.SerializeToString,
      ),
      'DiffConfig': grpc.unary_unary_rpc_method_handler(
          servicer.DiffConfig,
          request_deserializer=provider__pb2.DiffRequest.FromString,
          response_serializer=provider__pb2.DiffResponse.SerializeToString,
      ),
      'Configure': grpc.unary_unary_rpc_method_handler(
          servicer.Configure,
          request_deserializer=provider__pb2.ConfigureRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'Invoke': grpc.unary_unary_rpc_method_handler(
          servicer.Invoke,
          request_deserializer=provider__pb2.InvokeRequest.FromString,
          response_serializer=provider__pb2.InvokeResponse.SerializeToString,
      ),
      'Check': grpc.unary_unary_rpc_method_handler(
          servicer.Check,
          request_deserializer=provider__pb2.CheckRequest.FromString,
          response_serializer=provider__pb2.CheckResponse.SerializeToString,
      ),
      'Diff': grpc.unary_unary_rpc_method_handler(
          servicer.Diff,
          request_deserializer=provider__pb2.DiffRequest.FromString,
          response_serializer=provider__pb2.DiffResponse.SerializeToString,
      ),
      'Create': grpc.unary_unary_rpc_method_handler(
          servicer.Create,
          request_deserializer=provider__pb2.CreateRequest.FromString,
          response_serializer=provider__pb2.CreateResponse.SerializeToString,
      ),
      'Read': grpc.unary_unary_rpc_method_handler(
          servicer.Read,
          request_deserializer=provider__pb2.ReadRequest.FromString,
          response_serializer=provider__pb2.ReadResponse.SerializeToString,
      ),
      'Update': grpc.unary_unary_rpc_method_handler(
          servicer.Update,
          request_deserializer=provider__pb2.UpdateRequest.FromString,
          response_serializer=provider__pb2.UpdateResponse.SerializeToString,
      ),
      'Delete': grpc.unary_unary_rpc_method_handler(
          servicer.Delete,
          request_deserializer=provider__pb2.DeleteRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'Cancel': grpc.unary_unary_rpc_method_handler(
          servicer.Cancel,
          request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'GetPluginInfo': grpc.unary_unary_rpc_method_handler(
          servicer.GetPluginInfo,
          request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
          response_serializer=plugin__pb2.PluginInfo.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'pulumirpc.ResourceProvider', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
