import random
from concurrent import futures

import grpc
import user_statistics_pb2_grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
from user_statistics_pb2 import (
    Top10_Request,
    Top10_Response,
    MostUsedTopics_Request,
    MostUsedTopics_Response,
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

        responseList = self.anime_stub.MultipleAnimeByName(ar_pb2.multiple_anime_by_name_Request(anime_names=sorted_dict.values()))
        if responseList is None:
            return NotFound("Anime list not found")

        return Top10_Response(responseList)

    #TODO: AINDA NAO SEI COMO FUNCIONA O GETUSERPOSTS
    def GetMostUsedTopics(self, request, context):
        # Fetch the user making the request
        user = self.user_stub.GetUser(ur_pb2.get_user_Request(user_name=request.user_name))
        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

        # TODO: Nao sei se preciso de usar este ou não
        user_topics = user.topics_subscribed

        #TODO: Descobrir como obter os posts do utilizador
        # Fetch the posts made by the user
        posts = self.user_stub.GetUserPosts(ur_pb2.get_user_posts_Request(user_name=request.user_name))
        if not posts:
            context.abort(grpc.StatusCode.NOT_FOUND, "No posts found for the user")
            
        # Count the usage of each topic
        topic_usage = {}
        for post in posts:
            for topic in post.topics:
                if topic not in topic_usage:
                    topic_usage[topic] = 0
                topic_usage[topic] += 1

        sorted_topics = sorted(topic_usage.items(), key=lambda x: x[1], reverse=True)

        return MostUsedTopics_Response(sorted_topics[:10])
        
        

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