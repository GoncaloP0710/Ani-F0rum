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

