import wallet_pb2 as message
import wallet_pb2_grpc as service
import grpc

class WalletClient():
    def __init__(self):
        self.host = 'localhost'
        self.port = 50052

        self.channel = grpc.insecure_channel(
                        '{}:{}'.format(self.host, self.port))

        self.stub = service.WalletStub(self.channel)

    def top_up(self, phone_number, fromBank, amount):
        req = message.topupReq(phone_number=phone_number, fromBank=fromBank, amount=amount)
        return self.stub.TopUp(req)