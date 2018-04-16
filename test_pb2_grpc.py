# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import test_pb2 as test__pb2


class GreeterStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.newSession = channel.unary_unary(
        '/Greeter/newSession',
        request_serializer=test__pb2.sessionInquiry.SerializeToString,
        response_deserializer=test__pb2.newSessionNum.FromString,
        )
    self.append = channel.unary_unary(
        '/Greeter/append',
        request_serializer=test__pb2.appendRequest.SerializeToString,
        response_deserializer=test__pb2.appendReply.FromString,
        )
    self.addSeq = channel.unary_unary(
        '/Greeter/addSeq',
        request_serializer=test__pb2.addSeqRequest.SerializeToString,
        response_deserializer=test__pb2.addSeqReply.FromString,
        )


class GreeterServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def newSession(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def append(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def addSeq(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_GreeterServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'newSession': grpc.unary_unary_rpc_method_handler(
          servicer.newSession,
          request_deserializer=test__pb2.sessionInquiry.FromString,
          response_serializer=test__pb2.newSessionNum.SerializeToString,
      ),
      'append': grpc.unary_unary_rpc_method_handler(
          servicer.append,
          request_deserializer=test__pb2.appendRequest.FromString,
          response_serializer=test__pb2.appendReply.SerializeToString,
      ),
      'addSeq': grpc.unary_unary_rpc_method_handler(
          servicer.addSeq,
          request_deserializer=test__pb2.addSeqRequest.FromString,
          response_serializer=test__pb2.addSeqReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Greeter', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
