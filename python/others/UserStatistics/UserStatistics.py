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
    KarmaUpdateResponse,
    GetAllUsersResponse,
    GetUserByNameResponse,
)

from python.Common.User_pb2 import (
    Rarity,
    Achievement,
    User
)

from python.Common.Anime_pb2 import (
    Anime,
    AnimeGenre,
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
        self.user_channel = grpc.insecure_channel('user-repository:50043')  # Create a channel to the UserRepository
        self.user_stub = UserRepository_pb2_grpc.UserRepositoryStub(self.user_channel)

        self.anime_channel = grpc.insecure_channel('anime-repository:50053')  # Create a channel to the AnimeRepository
        self.anime_stub = AnimeRepository_pb2_grpc.AnimeRepositoryStub(self.anime_channel)

        self.topic_channel = grpc.insecure_channel('localhost:50062')  # Create a channel to the TopicRepository
        self.topic_stub = TopicRepository_pb2_grpc.TopicRepositoryStub(self.topic_channel)

    def GetTop10(self, request, context):
        
        response = self.user_stub.GetUser(UserRepository_pb2.get_user_Request(user_name=request.user_name))
        user = response.user
        if user is None:
            return NotFound("User not found")

        dict_list = dict(zip(user.anime_watched_score, user.animes_watched))
        #sorted_dict = sorted(dict_list)[:10]
        sorted_values = [value for _, value in sorted(dict_list.items(), key=lambda item: item[0], reverse=True)]
        sorted_values = sorted_values[:10]
        print("sorted")
        print(sorted_values)

        responseList = self.anime_stub.MultipleAnimeByName(AnimeRepository_pb2.multiple_anime_by_name_Request(anime_names=sorted_values))
        if responseList.animes is None:
            return NotFound("Anime list not found")
        print("response")
        print(responseList.animes)

        return Top10_Response(animes = responseList.animes)

    def GetMostUsedTopics(self, request, context):
        print("GetMostUsedTopics")

        response = self.user_stub.GetUser(UserRepository_pb2.get_user_Request(user_name=request.user_name))
        user = response.user
        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

        # Dicionário para contar a frequência de tópicos
        topic_count = {}
        topic_objects = {}

        # Iterar pelos tópicos do usuário
        for topic_name in user.topics_subscribed:
            # Buscar o objeto Topic do repositório
            response_topic = self.topic_stub.GetTopic(TopicRepository_pb2.GetTopicRequest(topicname=topic_name))
            topic = response_topic.topic
            if not topic:
                context.abort(grpc.StatusCode.NOT_FOUND, "Topic not found")

            # Salvar o objeto Topic no dicionário
            topic_objects[topic_name] = topic

            # Contar publicações feitas pelo usuário no tópico
            for publication in topic.publications:
                if publication.HasField("message") and publication.message.username == user.user_name:
                    if topic_name in topic_count:
                        topic_count[topic_name] += 1
                    else:
                        topic_count[topic_name] = 1
                elif publication.HasField("images") and publication.images.username == user.user_name:
                    if topic_name in topic_count:
                        topic_count[topic_name] += 1
                    else:
                        topic_count[topic_name] = 1

        # Ordenar os tópicos por frequência
        sorted_topics = sorted(topic_count.items(), key=lambda x: x[1], reverse=True)

        # Retornar os 10 tópicos mais usados como objetos Topic
        top_topics = [topic_objects[topic[0]] for topic in sorted_topics[:10]]
        return MostUsedTopics_Response(most_used_topics=top_topics)
    
    def GetUserKarma(self, request, context):
        response = self.user_stub.GetUser(UserRepository_pb2.get_user_Request(user_name=request.user_name))
        if not response.user:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

        return KarmaResponse(karma_Value=response.user.karma)
    
    def UpdateUserKarma(self, request, context):
        print("UpdateUserKarma")
        response = self.user_stub.UpdateUserKarma(UserRepository_pb2.update_user_karma_Request(user_name=request.user_name, karma_value=request.karma_value))
        if not response.success:
            context.abort(grpc.StatusCode.NOT_FOUND, "Failed to update user karma")

        return KarmaUpdateResponse(success=response.success)
        
    def GetAllUsers(self, request, context):
        print("GetAllUsers")
        response = self.user_stub.GetAllUsers(UserRepository_pb2.get_all_users_Request())
        user_list = response.users
        if not user_list:
            context.abort(grpc.StatusCode.NOT_FOUND, "No users found")

        return GetAllUsersResponse(users=user_list)
    
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

   
    server.add_insecure_port("[::]:50041")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()