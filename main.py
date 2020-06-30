from concurrent import futures
import logging

import grpc

import service_pb2
import service_pb2_grpc

#-----------------------------
import redis
import json

import pymongo
import os
import sys

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']
REDIS_PORT = os.environ['REDIS_PORT']
REDIS_AGES_LIST = os.environ['REDIS_AGES_LIST']
REDIS_LAST_ITEM = os.environ['REDIS_LAST_ITEM']

MONGO_HOST = os.environ['MONGO_HOST']
MONGO_USER = os.environ['MONGO_USER']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
MONGO_PORT = os.environ['MONGO_PORT']
MONGO_DB_NAME = os.environ['MONGO_DB']
MONGO_ITEMS_COLLECTION = os.environ['MONGO_ITEMS_COLLECTION']

class gRPCServer(service_pb2_grpc.DataServicer):

    def SendData(self, request, context):
        print('Data: %s' % request.data)
        res = saveData(request.data)
        return service_pb2.SendDataReply(message=res)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_DataServicer_to_server(gRPCServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Esperando peticiones...")
    server.wait_for_termination()

def saveData(data):
    try:        
        item = json.loads(data)            
        #Redis
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)
        #Se guarda el ultimo item insertado en Redis
        #r.hmset(REDIS_LAST_ITEM, item) #deprecated usar hset en lugar de hmset
        r.hset(REDIS_LAST_ITEM, "Nombre", item["Nombre"])
        r.hset(REDIS_LAST_ITEM, "Departamento", item["Departamento"])
        r.hset(REDIS_LAST_ITEM, "Edad", item["Edad"])
        r.hset(REDIS_LAST_ITEM, "Forma de contagio", item["Forma de contagio"])
        r.hset(REDIS_LAST_ITEM, "Estado", item["Estado"])
        #Se agrega la edad del ultimo item insertado en la lista de edades en Redis
        r.rpush(REDIS_AGES_LIST, item["Edad"])

        #mongo
        client = pymongo.MongoClient('mongodb://%s:%s@%s:%s' %(MONGO_USER, MONGO_PASSWORD,MONGO_HOST, MONGO_PORT))
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_ITEMS_COLLECTION]
        #Se inserta el item en mongo, en la coleccion items
        x = collection.insert_one(item)
        return 'ok'
    except Exception as e:            
        print("Unexpected error:", sys.exc_info()[0])
        if hasattr(e, 'message'):
            print("Error  inesperado: " + e.message)
        
        return "Unexpected error:", sys.exc_info()[0]


if __name__ == '__main__':
    logging.basicConfig()
    serve()