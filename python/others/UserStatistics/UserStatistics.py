import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from concurrent import futures

import grpc
from python.others.UserStatistics.UserStatistics_pb2_grpc import(
    UserStatisticsService,
    add_UserStatisticsServiceServicer_to_server,
)
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
from UserStatistics_pb2 import (
    Top10_Response,
    MostUsedTopics_Response,
    MostUsedTopics_Request,
    KarmaResponse,
    KarmaRequest,
    GetAllUsersResponse,
    GetUserByNameResponse,
)

from python.Common.User_pb2 import (
    Rarity,
    Achievement,
    User
)

from python.Common.Topic_pb2 import (
    Subscriber,
    Message,
    Image,
    Publication,
    Topic,
)

from python.repository.User import UserRepository_pb2_grpc
from python.repository.User import UserRepository_pb2 
from python.repository.Anime import AnimeRepository_pb2_grpc
from python.repository.Anime import AnimeRepository_pb2 
from python.repository.Topic import TopicRepository_pb2_grpc
from python.repository.Topic import TopicRepository_pb2

class UserStatistics(UserStatisticsService):

    def __init__(self):
        self.user_channel = grpc.insecure_channel('localhost:50043')  # Create a channel to the UserRepository
        self.user_stub = UserRepository_pb2_grpc.UserRepositoryStub(self.user_channel)

        self.anime_channel = grpc.insecure_channel('localhost:50053')  # Create a channel to the AnimeRepository
        self.anime_stub = AnimeRepository_pb2_grpc.AnimeRepositoryStub(self.anime_channel)

        self.topic_channel = grpc.insecure_channel('localhost:50062')  # Create a channel to the TopicRepository
        self.topic_stub = TopicRepository_pb2_grpc.TopicRepositoryStub(self.topic_channel)

    def GetTop10(self, request, context):
        
        response = self.user_stub.GetUser(UserRepository_pb2.get_user_Request(user_name=request.user_name))
        user = response.user
        if user is None:
            return NotFound("User not found")

        dict_list = dict(zip(user.anime_watched_score, user.animes_watched))
        sorted_dict = sorted(dict_list)[:10]

        responseList = self.anime_stub.MultipleAnimeByName(AnimeRepository_pb2.multiple_anime_by_name_Request(anime_names=sorted_dict.values()))
        if responseList.animes is None:
            return NotFound("Anime list not found")

        return Top10_Response(animes = responseList.animes)

    def GetMostUsedTopics(self, request, context):
        print("GetMostUsedTopics")

        response = self.user_stub.GetUser(UserRepository_pb2.get_user_Request(user_name=request.user_name))
        user = response.user
        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

         # Dicionário para contar a frequência de tópicos
        topic_count = {}

        # Iterar pelos tópicos do usuário
        for topic_name in user.topics:

            response_topic = self.topic_stub.GetTopic(TopicRepository_pb2.GetTopicRequest(topicname=topic_name))
            topic = response_topic.topic
            if not topic:
                context.abort(grpc.StatusCode.NOT_FOUND, "Topic not found")

            for publication in topic.publications:
                # Verificar se a publicação foi feita pelo usuário
                if publication.message.username == user.user_name:
                    topic_name = topic.topicname
                    if topic_name in topic_count:
                        topic_count[topic_name] += 1
                    else:
                        topic_count[topic_name] = 1

        sorted_topics = sorted(topic_count.items(), key=lambda x: x[1], reverse=True)

        # Retornar os 10 tópicos mais usados
        top_topics = [topic[0] for topic in sorted_topics[:10]]
        return MostUsedTopics_Response(most_used_topics=top_topics)
    
    def GetUserKarma(self, request, context):
        response = self.user_stub.GetUser(UserRepository_pb2.get_user_Request(user_name=request.user_name))
        if not response.user:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

        return KarmaResponse(karma_Value=response.user.karma)
        
    def GetAllUsers(self, request, context):
        print("GetAllUsers")
        response = self.user_stub.GetAllUsers(UserRepository_pb2.get_all_users_Request())
        user = response.user
        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, "No users found")

        return GetAllUsersResponse(users=user.users)
    
    def GetUserByName(self, request, context):
        print("GetUserByName")
        response = self.user_stub.GetUser(UserRepository_pb2.get_user_Request(user_name=request.user_name))
        if not response.user:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

        return GetUserByNameResponse(user=response.user)

#TODO
def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_UserStatisticsServiceServicer_to_server(
        UserStatistics(), server
    )

   
    server.add_insecure_port("[::]:50060")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()