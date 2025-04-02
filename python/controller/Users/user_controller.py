import sys
import os
import connexion
import pathlib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

basedir = pathlib.Path(__file__).parent.resolve()

connex_app = connexion.App(__name__, specification_dir=basedir)
connex_app.add_api(basedir / "swagger.yml")

import grpc
from python.others.UserRecommendations import UserRecommendations_pb2_grpc, UserRecommendations_pb2
from python.others.AnimeList import AnimeList_pb2_grpc, AnimeList_pb2
from python.Common import User_pb2 as Common_dot_User__pb2
from python.others.UserStatistics import UserStatistics_pb2_grpc, UserStatistics_pb2

def get_related_by_anime(user_name):
    # TODO: once the operation to get the animes watched by the user is tested use it instead.
    animes_name_watched = ["Naruto", "One Piece"]
    animes_watched = []
    similar_animes = []

    print(animes_name_watched)

    try:
        with grpc.insecure_channel('localhost:50052') as channel:
            stub = AnimeList_pb2_grpc.AnimeListStub(channel)
            request = AnimeList_pb2.get_multiple_anime_by_name_Request(anime_names=animes_name_watched)
            response = stub.GetMultipleAnimeByName(request)
            animes_watched = response.animes

            for anime in animes_name_watched:
                request = AnimeList_pb2.get_similar_anime_Request(anime_name=anime)
                response = stub.GetSimilarAnime(request)
                similar_animes += response.animes

        # Remove duplicates by using a dictionary keyed by anime name
        unique_animes = {}
        for anime in similar_animes:
            if anime.name not in unique_animes:
                unique_animes[anime.name] = anime
        similar_animes = list(unique_animes.values())

        print ("=========================== Animes Watched =====================")
        print (animes_watched)
        print ("=========================== Animes Similar =====================")
        print (similar_animes)

        with grpc.insecure_channel('localhost:50042') as channel:
            stub = UserRecommendations_pb2_grpc.UserRecommendationsStub(channel)
            request = UserRecommendations_pb2.users_related_by_anime_Request(
                animes_watched=animes_watched, animes_similar=similar_animes
            )
            response = stub.GetUsersRelatedByAnime(request)

            # Convert User objects to JSON-serializable dictionaries
            users_related_by_anime = [
                {
                    "user_name": user.user_name,
                    "location": user.location if user.HasField("location") else None,
                    "animes_watched": list(user.animes_watched),
                    "anime_watched_score": list(user.anime_watched_score),
                    "topics_subscribed": list(user.topics_subscribed),
                    "karma": user.karma,
                    "achievements": [
                        {
                            "title": achievement.title,
                            "description": achievement.description,
                            "date": achievement.date,
                            "rarity": achievement.rarity,
                        }
                        for achievement in user.achievements
                    ],
                }
                for user in response.users
            ]

            print ("=========================== Animes Similar =====================")

            print (users_related_by_anime)

            return {"users_related_by_anime": users_related_by_anime}

    except grpc.RpcError as e:
        return {"error": f"RPC failed: {e}"}, 500


def all_users():
    try:
        with grpc.insecure_channel('localhost:50060') as channel:
            stub = UserStatistics_pb2_grpc.UserStatisticsServiceStub(channel)
            request = UserStatistics_pb2.Empty()
            response = stub.GetAllUsers(request)
            return {
                "users": [
                    {
                        "user_name": user.user_name,
                        "location": user.location if user.HasField("location") else None,
                        "animes_watched": list(user.animes_watched),
                        "anime_watched_score": list(user.anime_watched_score),
                        "topics_subscribed": list(user.topics_subscribed),
                        "karma": user.karma,
                        "achievements": [
                            {
                                "title": achievement.title,
                                "description": achievement.description,
                                "date": achievement.date,
                                "rarity": achievement.rarity,
                            }
                            for achievement in user.achievements
                        ],
                    }
                    for user in response.users
                ]
            }
    except grpc.RpcError as e:
        return {"error": f"RPC failed: {e}"}, 500


def get_user(user_name):
    try:
        with grpc.insecure_channel('localhost:50060') as channel:
            stub = UserStatistics_pb2_grpc.UserStatisticsServiceStub(channel)
            request = UserStatistics_pb2.GetUserByNameRequest(user_name=user_name)
            response = stub.GetUserByName(request)
            user = response.user
            return {
                "user": {
                    "user_name": user.user_name,
                    "location": user.location if user.HasField("location") else None,
                    "animes_watched": list(user.animes_watched),
                    "anime_watched_score": list(user.anime_watched_score),
                    "topics_subscribed": list(user.topics_subscribed),
                    "karma": user.karma,
                    "achievements": [
                        {
                            "title": achievement.title,
                            "description": achievement.description,
                            "date": achievement.date,
                            "rarity": achievement.rarity,
                        }
                        for achievement in user.achievements
                    ],
                }
            }
    except grpc.RpcError as e:
        return {"error": f"RPC failed: {e}"}, 500


def get_karma(user_name):
    try:
        with grpc.insecure_channel('localhost:50060') as channel:
            stub = UserStatistics_pb2_grpc.UserStatisticsServiceStub(channel)
            request = UserStatistics_pb2.KarmaRequest(user_name=user_name)
            response = stub.GetUserKarma(request)
            return {"karma": list(response.karma)}
    except grpc.RpcError as e:
        return {"error": f"RPC failed: {e}"}, 500


def top10Anime(user_name):
    try:
        with grpc.insecure_channel('localhost:50060') as channel:
            stub = UserStatistics_pb2_grpc.UserStatisticsServiceStub(channel)
            request = UserStatistics_pb2.Top10_Request(user_name=user_name)
            response = stub.GetTop10(request)
            return {"top10_anime": list(response.anime)}
    except grpc.RpcError as e:
        return {"error": f"RPC failed: {e}"}, 500


def list_topics(user_name):
    try:
        with grpc.insecure_channel('localhost:50060') as channel:
            stub = UserStatistics_pb2_grpc.UserStatisticsServiceStub(channel)
            request = UserStatistics_pb2.MostUsedTopicsRequest(user_name=user_name)
            response = stub.GetMostUsedTopics(request)
            return {"topics": list(response.topics)}
    except grpc.RpcError as e:
        return {"error": f"RPC failed: {e}"}, 500


if __name__ == "__main__":
    connex_app.run(host="0.0.0.0", port=50040)
