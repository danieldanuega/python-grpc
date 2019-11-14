Python gRPC

Hi there this is the easy implementation of gRPC in python.
It is cover up some gRPC fundamental and this tutorial use MySQL to get familiar with db connection in grpc

The database host inside GCP Cloud SQL, you can change to localhost if you want.

Bash command for generate grpc file:
`python -m grpc_tools.protoc --proto_path=. ./wallet.proto --python_out=. --grpc_python_out=.`
