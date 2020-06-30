from __future__ import print_function
import logging

import grpc

import service_pb2
import service_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code
    data = '{"Nombre": "Mario Martinez", "Departamento": "Jutiapa", "Edad": 38, "Forma de contagio": "Comunitario", "Estado": "Activo"}'
    
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.DataStub(channel)
        response = stub.SendData(service_pb2.SendDataRequest(data=data))
    print("gRPC client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()