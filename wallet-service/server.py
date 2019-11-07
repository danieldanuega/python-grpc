import wallet_pb2 as message
import wallet_pb2_grpc as service

from client_users import UsersClient

from concurrent import futures
import time
import grpc
from config import mongo
import pymongo

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
user_svc = UsersClient()


class WalletService(service.WalletServicer):
    def TopUp(self, request, context):
        premium = user_svc.check_premium(request.phone_number).status
        if premium:
            mongo.update(
                {'phone_number': request.phone_number},
                {'$inc': {'balance': request.amount}}
            )
            return message.statusRes(status=True, msg="Sukses mentransfer")
        elif not premium:
            return message.statusRes(status=False, msg="User bukan premium atau tidak ditemukan")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service.add_WalletServicer_to_server(WalletService(), server)
    server.add_insecure_port('127.0.0.1:50052')
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