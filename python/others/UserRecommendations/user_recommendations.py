import sys
import os
import random
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
    recomended_animeList_by_topics_Response,
)

# TODO: Change that latter for the correct import
from python.Common.User_pb2 import (
    User,
) 

from python.repository.User import UserRepository_pb2
from python.repository.User import UserRepository_pb2_grpc

class UserRecommendations_Service(UserRecommendationsServicer):

    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50063')  # Create a channel to the UserRepository
        self.stub = UserRepository_pb2_grpc.UserServiceStub(self.channel)

    # Used when user wants to get other users related by anime
    # It should be called after getting similar animes to the ones the user watched
    def GetUsersRelatedByAnime(self, request, context):
        try:
            user_scores = {}
            weight_watched = 1.7  # Higher weight for animes_watched
            weight_similar = 1  # Lower weight for animes_similar

            # Process animes_watched
            response = self.stub.GetUsersThatWatchedAnime(
                UserRepository_pb2.get_users_that_watched_anime_Request(anime_names=[request.animes_watched])
            )
            for user in response.users:
                if user.user_name not in user_scores:
                    user_scores[user.user_name] = 0
                user_scores[user.user_name] += weight_watched

            # Process animes_similar
            response = self.stub.GetUsersThatWatchedAnime(
                UserRepository_pb2.get_users_that_watched_anime_Request(anime_names=[request.animes_similar])
            )
            for user in response.users:
                if user.user_name not in user_scores:
                    user_scores[user.user_name] = 0
                user_scores[user.user_name] += weight_similar

            # Sort users by their scores in descending order
            sorted_users = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)

            # Retrieve full user objects for the sorted user names, limiting to 10 users
            users = []
            for user_name, _ in sorted_users[:10]:  # Limit to the first 10 users
                user_response = self.stub.GetUser(
                    UserRepository_pb2.get_user_Request(user_name=user_name)
                )
                users.append(user_response.user)

            # Return the response
            return users_related_by_anime_Response(users=users)

        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
        
    def GetUsersRelatedByMessage(self, request, context):
        # TODO: create a method to get users related by message
        pass

    def GetUsersRelatedByTopics(self, request, context):
        # TODO: create a method to get users related by topics
        pass

    def GetRecomendedAnimeListByTopics(self, request, context):
        try:
            topics = request.topicsnames_submitted

            response = self.stub.GetAllAnime(
                UserRepository_pb2.get_all_anime_Request()
            )

            recommended_anime_list = []
            for anime in response.anime_list:
                if anime.name in topics or anime.genre in topics:
                    recommended_anime_list.append(anime)

            if len(recommended_anime_list) > 10:
                recommended_anime_list = random.sample(recommended_anime_list, 10)

            return recomended_animeList_by_topics_Response(anime_list=recommended_anime_list)
        
        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_UserRecommendationsServicer_to_server(
        UserRecommendations_Service(), server
    )
    server.add_insecure_port('[::]:50062')
    server.start()
    print('UserRecommendations server running on port 50062')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()