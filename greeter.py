from concurrent import futures
import time

import grpc
import test_pb2 as test_pb2
import test_pb2_grpc as test_pb2_grpc
import matching2 as matching

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

corpus = [
          (['QQ', 'DD', 'QQ', 'QQ', 'QQ', 'DD', 'AA', 'KK', 'QQ', 'DD', 'AA', 'QQ'], 'A'), # 1 Hyunwoo
          (['QQ', 'DD', 'QQ', 'QQ', 'QQ', 'QQ', 'AA', 'DD', 'QQ', 'DD', 'AA', 'KK'], 'A'), # 2 Jean
          (['QQ', 'DD', 'QQ', 'DD', 'QQ', 'CC', 'AA', 'DD', 'QQ', 'DD', 'AA', 'QQ'], 'A'), # 3 Eunyeong
          (['QQ', 'DD', 'QQ', 'DD', 'QQ', 'KK', 'AA', 'KK', 'QQ', 'DD', 'AA', 'KK'], 'A'), # 4 Seoyoung
          (['QQ', 'DD', 'QQ', 'DD', 'QQ', 'CD', 'AA', 'KK', 'QQ', 'QQ', 'AA', 'KK'], 'B'), # 5 SC
          (['QQ', 'DD', 'QQ', 'DD', 'QQ', 'DD', 'AA', 'KK', 'QQ', 'DD', 'AA', 'KK'], 'B'), # 6 Paul
          (['QQ', 'DD', 'QQ', 'DD', 'QQ', 'KK', 'AA', 'KK', 'QQ', 'DD', 'AA', 'KK'], 'B'), # 7 Jiyoun
          (['QQ', 'DD', 'QQ', 'AA', 'QQ', 'DD', 'AA', 'KK', 'QQ', 'DD', 'AA', 'KK'], 'B')  # 8 KJ
]

session = {}
sessionnum = 1


class Greeter(test_pb2_grpc.GreeterServicer):

  def newSession(self, request, context):
    global sessionnum
    session[str(sessionnum)] = matching.seqmap(corpus, '')
    return test_pb2.newSessionNum(sessionNum=sessionnum)

  def append(self, request, context):
    session['1'].append(request.label)
    maxval = session['1']._max()
    session['1'].print()
    return test_pb2.appendReply(message=str(maxval))

  def addSeq(self, request, context):
    # Protocol for appending seq
    # Type.QQ DD ...
    # The seq must be a space separated seq
    try:
        type, sequence = request.message.split('.')
        sequence = sequence.split(' ')
        print(type, sequence)
        corpus.append((sequence, type))
        print(corpus)
        return test_pb2.addSeqReply(message='OK')
    except:
        return test_pb2.addSeqReply(message='FAIL')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
  serve()
