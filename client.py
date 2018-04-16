from __future__ import print_function

import grpc

import test_pb2 as test_pb2
import test_pb2_grpc as test_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = test_pb2_grpc.GreeterStub(channel)
sessionnum = 0;

def run():
  response = stub.newSession(test_pb2.sessionInquiry(nonce=1))
  global sessionnum
  sessionnum = response.sessionNum
  print("Greeter client received: " + str(response.sessionNum))
  response = stub.append(test_pb2.appendRequest(sessionNum=sessionnum, label='QQ'))
  print("Greeter client received: " + response.message)

run()
while(True):
  s = input()
  if s[0] == '*':
      response = stub.addSeq(test_pb2.addSeqRequest(message=s[2:]))
      print("Greeter client received: " + response.message)
  else:
    response = stub.append(test_pb2.appendRequest(sessionNum=sessionnum, label=s))
    print("Greeter client received: " + response.message)
