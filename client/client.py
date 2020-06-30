from __future__ import print_function
import logging

import grpc

import service_pb2
import service_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.ServerStub(channel)
        response = stub.SayHello(service_pb2.HelloRequest(name='you'))
    print("gRPC client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()