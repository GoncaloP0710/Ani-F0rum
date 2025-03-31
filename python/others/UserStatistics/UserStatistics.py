from concurrent import futures

import grpc
import UserStatistics_pb2_grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
from UserStatistics_pb2 import (
    Top10_Request,
    Top10_Response,
    MostUsedTopics_Request,
    MostUsedTopics_Response,
    KarmaResponse,
    GetAllUsersResponse,
    GetUserByNameRequest,
    GetUserByNameResponse,
)

from python.repository.User import UserRepository_pb2_grpc as ur_grpc
from python.repository.User import UserRepository_pb2 as ur_pb2
from python.repository.Anime import AnimeRepository_pb2_grpc as ar_grpc
from python.repository.Anime import AnimeRepository_pb2 as ar_pb2

class UserStatistics(UserStatistics_pb2_grpc.UserStatisticsServicer):

    def __init__(self):
        self.user_channel = grpc.insecure_channel('localhost:50043')  # Create a channel to the UserRepository
        self.user_stub = ur_grpc.UserRepositoryStub(self.user_channel)

        self.anime_channel = grpc.insecure_channel('localhost:50053')  # Create a channel to the AnimeRepository
        self.anime_stub = ar_grpc.AnimeRepositoryStub(self.anime_channel)

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

    def GetMostUsedTopics(self, request, context):

        user = self.user_stub.GetUser(ur_pb2.get_user_Request(user_name=request.user_name))
        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

        posts = self.user_stub.GetUserPosts(ur_pb2.get_user_posts_Request(user_name=request.user_name))
        if not posts:
            context.abort(grpc.StatusCode.NOT_FOUND, "No posts found for the user")

        topic_usage = {}
        for post in posts:
            for topic in post.topics:
                if topic not in topic_usage:
                    topic_usage[topic] = 0
                topic_usage[topic] += 1

        sorted_topics = sorted(topic_usage.items(), key=lambda x: x[1], reverse=True)

        return MostUsedTopics_Response(sorted_topics[:10])
    
    def GetUserKarma(self, request, context):

        user = self.user_stub.GetUser(ur_pb2.get_user_Request(user_name=request.user_name))
        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

        user_posts = self.user_stub.GetUserPosts(ur_pb2.get_user_posts_Request(user_name=request.user_name))
        if not user_posts:
            context.abort(grpc.StatusCode.NOT_FOUND, "No posts found for the user")

        topic_popularity = set()
        for post in user_posts.posts:
            topic_name = post.topic_name
            if topic_name not in topic_popularity:
                topic_details = self.topic_stub.GetTopic(ur_pb2.get_topic_Request(topic_name=topic_name))
                topic_popularity[topic_name] = len(topic_details.subscribers)

        karma = 0
        for post in user_posts.posts:
            topic_name = post.topic_name
            karma += 1 * topic_popularity.get(topic_name, 1) 

        return KarmaResponse(karma_Value=karma)
        
    def GetAllUsers(self, request, context):
        user = self.user_stub.GetAllUsers(ur_pb2.get_all_users_Request())
        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, "No users found")

        return GetAllUsersResponse(users=user.users)
    
    def GetUserByName(self, request, context):
        user = self.user_stub.GetUser(ur_pb2.get_user_Request(user_name=request.user_name))
        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

        return GetUserByNameResponse(user=user)

#TODO
def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    UserStatistics_pb2_grpc.add_UserStatisticsServicer_to_server(
        UserStatistics(), server
    )

   
    server.add_insecure_port("[::]:50060")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()