from concurrent import futures
import time
import grpc
from config import mongo
import pymongo

import users_pb2_grpc as service
import users_pb2 as message

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class UsersService(service.UsersServicer):

    def CreateUser(self, request, context):
        user = request.user
        # Implement Insert PyMongo
        mongo.insert_one(
            {'phone_number': user.phone_number, 'firstname': user.firstname, 'lastname': user.lastname}
        )
        if mongo.find_one({'phone_number': user.phone_number}):
            return message.StatusRes(status="Successfuly created!")
        return message.StatusRes(status="Failed to insert user!")

    def MakePremium(self, request, context):
        user = mongo.find_one({'phone_number': request.phone_number})

        if user:
            mongo.update_one(
                {'phone_number': request.phone_number}, 
                {'$set': {'premium': True}}
            )
            return message.MPResponse(status="Success!", firstname=user['firstname'], lastname=user['lastname'])
        else:
            return message.MPResponse(status="Failed", firstname="NULL", lastname="NULL")

    def DeleteUser(self, request, context):
        if mongo.find_one({'phone_number': request.phone_number}):
            mongo.delete_one(
                {'phone_number': request.phone_number}
            )
            return message.StatusRes(status="SSkuuyyy")
        else:
            return message.StatusRes(status="No User found")

    def checkPremium(self, request, context):
        user = mongo.find_one({'phone_number': request.phone_number})
        if user:
            if mongo.find_one({'$and': [{'phone_number': {'$in': [request.phone_number]}}, {'premium': {'$exists': True}}]}):
                return message.CheckRes(status=True, msg="User is premium")
            else:
                return message.CheckRes(status=False, msg="User is not premium")
        else:
            return message.CheckRes(status=False, msg="User not found")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service.add_UsersServicer_to_server(UsersService(), server)
    server.add_insecure_port('127.0.0.1:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print('Srever Stop')
        server.stop(0)

if __name__ == '__main__':
    print('Server Start')
    serve()