import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from python.others.UserRecommendations.UserRecommendations_pb2_grpc import (
    UserRecommendationsServicer,
    add_UserRecommendationsServicer_to_server,
)
from python.others.UserRecommendations.UserRecommendations_pb2 import (
    users_related_by_anime_Response,
    users_related_by_message_Response,
    users_related_by_topics_Response,
    recomended_animeList_Response,
    recomended_animeList_by_topics_Response,
)

from python.Common.User_pb2 import (
    User,
    Rarity,
    Achievement,
)

from python.services.User import UserService_pb2
from python.services.User import UserService_pb2_grpc

class UserRecommendations_Service(UserRecommendationsServicer):

    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50055')  # Create a channel to the UserRepository
        self.stub = UserService_pb2_grpc.UserServiceStub(self.channel)

    def GetUsersRelatedByAnime(self, request, context):
        # TODO: create a method to get users related by anime
        pass

    def GetUsersRelatedByMessage(self, request, context):
        # TODO: create a method to get users related by message
        pass

    def GetUsersRelatedByTopics(self, request, context):
        # TODO: create a method to get users related by topics
        pass

    def GetRecomendedAnimeList(self, request, context):
        # TODO: create a method to get recomended anime list
        pass

    def GetRecomendedAnimeListByTopics(self, request, context):
        # TODO: create a method to get recomended anime list by topics
        pass


def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_UserRecommendationsServicer_to_server(
        UserRecommendations_Service(), server
    )
    server.add_insecure_port('[::]:50056')
    server.start()
    print('UserRecommendations server running on port 50056')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()