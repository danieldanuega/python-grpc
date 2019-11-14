import wallet_pb2 as message
import wallet_pb2_grpc as service

from client_users import UsersClient

from concurrent import futures
import time
import grpc
from config import conn

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
user_svc = UsersClient()


class WalletService(service.WalletServicer):

    # TO-DO: Still cannot write into DB `status: "%d format: a number is required, not str"`
    def TopUp(self, request, context):
        try:
            premium = user_svc.check_premium(request.phone_number).status
            try:
                with conn.cursor() as cursor:
                    if premium == '1':
                        sql = "UPDATE card SET balance = balance + %d WHERE phone_number = %s"
                        exe = cursor.execute(sql, (request.amount, request.phone_number))
                        return message.StatusRes(status=str(exe))
                    elif premium == '0':
                        return message.StatusRes(status='Belum Premium')

            except Exception as e:
                result = message.StatusRes(status=str(e))
        except Exception as e:
            result = message.StatusRes(status="Tidak ketemu")

        conn.commit()
        return result


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