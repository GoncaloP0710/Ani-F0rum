import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from python.repository.User.UserRepository_pb2_grpc import (
    UserRepositoryServicer,
    add_UserRepositoryServicer_to_server,
)
from python.repository.User.UserRepository_pb2 import (
    get_user_Response,
    get_all_users_Response,
    get_users_that_watched_anime_Response,
)

# TODO: Change that latter for the correct import
from python.Common.User_pb2 import (
    User,
)

class UserRepository_Service(UserRepositoryServicer) :

    # TODO: Implement database connection and queries to retrieve user database

    # Returns an user by name
    def GetUser(self, request, context):
        print("Searching for user with id: ", request.user_name)
        return get_user_Response(user=User())

    # Returns all users
    def GetAllUsers(self, request, context):
        print("Searching for all users")
        return get_all_users_Response(users=[])
    
    # Returns all users with one of the animes in their list
    def GetUsersThatWatchedAnime(self, request, context):
        print("Searching for users that watched this animes: ", request.anime_names)
        return get_users_that_watched_anime_Response(users=[])

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_UserRepositoryServicer_to_server(
        UserRepository_Service(), server
    )
    server.add_insecure_port('[::]:50054')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
