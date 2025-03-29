import random
from concurrent import futures

import grpc
import user_statistics_pb2_grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
from user_statistics_pb2 import (
    Top10_Request,
    Top10_Response,
)

from python.repository.User import UserRepository_pb2_grpc as ur_grpc
from python.repository.User import UserRepository_pb2 as ur_pb2
from python.repository.Anime import AnimeRepository_pb2_grpc as ar_grpc
from python.repository.Anime import AnimeRepository_pb2 as ar_pb2

class user_statistics(user_statistics_pb2_grpc.user_statisticsServicer):

    def __init__(self):
        self.user_channel = grpc.insecure_channel('localhost:50054')  # Create a channel to the UserRepository
        self.user_stub = user_statistics_pb2_grpc.UserStatisticsService(self.user_channel)

        self.anime_channel = grpc.insecure_channel('localhost:50053')  # Create a channel to the AnimeRepository
        self.anime_stub = user_statistics_pb2_grpc.UserStatisticsService(self.anime_channel)

    def GetTop10(self, request, context):
        
        user = self.user_stub.GetUser(ur_pb2.get_user_Request(user_name=request.user_name))
        if user is None:
            return NotFound("User not found")

        dict_list = dict(zip(user.anime_watched_score, user.animes_watched))
        sorted_dict = sorted(dict_list)[:10]

        return Top10_Response(sorted_dict[:10])

        

#TODO
def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    achievements_pb2_grpc.add_AchievementsServicer_to_server(
        Achievements(), server
    )

   
    server.add_insecure_port("[::]:443")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()