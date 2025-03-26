import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from python.services.User.UserService_pb2_grpc import (
    UserServiceServicer,
    add_UserServiceServicer_to_server,
)
from python.services.User.UserService_pb2 import (
    get_user_Response,
    users_related_by_anime_Response,
)

# TODO: Change that latter for the correct import
from python.Common.User_pb2 import (
    User,
) 

from python.repository.User import UserRepository_pb2
from python.repository.User import UserRepository_pb2_grpc

class UserService_Service(UserServiceServicer):

    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50054')  # Create a channel to the UserRepository
        self.stub = UserRepository_pb2_grpc.UserRepositoryStub(self.channel)

    def GetUser(self, request, context):
        try:
            response = self.stub.GetUser(UserRepository_pb2.get_user_Request(user_name=request.user_name))
            return get_user_Response(user=response.user)
        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
    
    def GetAllUsers(self, request, context):
        try:
            response = self.stub.GetAllUsers(UserRepository_pb2.get_all_users())
            return get_user_Response(users=response.users)
        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
    
    def GetUsersRelatedByAnime(self, request, context):
        try:
            response = self.stub.GetUsersRelatedByAnime(UserRepository_pb2.users_related_by_anime_Request(anime_names=request.anime_names))
            return users_related_by_anime_Response(users=response.users)
        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_UserServiceServicer_to_server(
        UserService_Service(), server
    )
    server.add_insecure_port('[::]:50055')
    server.start()
    print("UserService server running on port 50055")
    server.wait_for_termination()   

if __name__ == '__main__':
    serve()