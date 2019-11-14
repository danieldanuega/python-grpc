from concurrent import futures
import time
import grpc
import pymysql
from config import conn

import users_pb2_grpc as service
import users_pb2 as message

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class UsersService(service.UsersServicer):

    def CreateUser(self, request, context):
        user = request.user
        
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO `user_acc` (`phone_number`,`firstname`,`lastname`) VALUES (%s,%s,%s)"
                exe = cursor.execute(sql, (user.phone_number, user.firstname, user.lastname))
                result = message.StatusRes(status=str(exe))
        except Exception as e:
            result = message.StatusRes(status=str(e))
        
        conn.commit()
        return result


    def MakePremium(self, request, context):
        try:
            with conn.cursor() as cursor:
                sql = "SELECT `is_premium`, `firstname`, `lastname` FROM `user_acc` WHERE `phone_number`=%s"
                cursor.execute(sql, (request.phone_number))
                check = cursor.fetchone()

                if check['is_premium'] == 0:
                    sql = "UPDATE `user_acc` SET `is_premium`=1 WHERE `phone_number`=%s"
                    exe = cursor.execute(sql, (request.phone_number))
                    result = message.StatusRes(status=str(exe))
            
        except Exception as e:
            result = message.StatusRes(status=str(e))
        
        conn.commit()
        return result
            

    def DeleteUser(self, request, context):
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM `user_acc` WHERE `phone_number`=%s"
                exe = cursor.execute(sql, (request.phone_number))
                result = message.StatusRes(status=str(exe)) 
        except Exception as e:
            result = message.StatusRes(status=str(e))

        conn.commit()
        return result

    def checkPremium(self, request, context):
        try:
            with conn.cursor() as cursor:
                sql = "SELECT `is_premium` FROM user_acc WHERE `phone_number`=%s"
                exe = cursor.execute(sql, (request.phone_number))
                check = cursor.fetchone()
                if check['is_premium'] == 1:
                    result = message.StatusRes(status='1')
                elif check['is_premium'] == 0:
                    result = message.StatusRes(status='0')
        except Exception as e:
            result = message.StatusRes(status=str(e))

        return result

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
    conn.close()