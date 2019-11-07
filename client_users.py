import users_pb2 as message
import users_pb2_grpc as service
import grpc

class UsersClient():
    def __init__(self):
        self.host = 'localhost'
        self.port = 50051

        self.channel = grpc.insecure_channel(
                        '{}:{}'.format(self.host, self.port))

        self.stub = service.UsersStub(self.channel)

    def create_user(self, phone_number, firstname, lastname):
        user = message.User(phone_number=phone_number, firstname=firstname, lastname=lastname)
        req = message.UserReq(user=user)
        return self.stub.CreateUser(req)

    def make_premium(self, phone_number):
        req = message.PhoneNumReq(phone_number=phone_number)
        return self.stub.MakePremium(req)

    def delete_user(self, phone_number):
        req = message.PhoneNumReq(phone_number=phone_number)
        return self.stub.DeleteUser(req)

    def check_premium(self, phone_number):
        req = message.PhoneNumReq(phone_number=phone_number)
        return self.stub.checkPremium(req)