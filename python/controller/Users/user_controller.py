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
from python.others.Achievements import Achievements_pb2_grpc, Achievements_pb2
from python.others.FeedGenerator import FeedGenerator_pb2_grpc, FeedGenerator_pb2

def get_related_by_anime(user_name):
    top10_response = top10Anime(user_name)
    animes_name_watched = [anime['name'] for anime in top10_response['top10_anime']]
    animes_watched = []
    similar_animes = []

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
            return {"karma": response.karma_Value}
    except grpc.RpcError as e:
        return {"error": f"RPC failed: {e}"}, 500


def top10Anime(user_name):
    try:
        with grpc.insecure_channel('localhost:50060') as channel:
            stub = UserStatistics_pb2_grpc.UserStatisticsServiceStub(channel)
            request = UserStatistics_pb2.Top10_Request(user_name=user_name)
            response = stub.GetTop10(request)
           
            # Retornar uma lista de animes hardcoded
        return {
            "top10_anime": [
                {
                    "name": anime.name,
                    "genres": list(anime.genres),
                    "episodes": anime.episodes,
                    "score": anime.score,
                    "aired": anime.aired,
                    "synopsis": anime.synopsis,
                }
                for anime in response.animes
            ]
        }
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
    
def get_user_achievements_list(user_name):
    try:
        with grpc.insecure_channel('localhost:50080') as channel:  # Connect to the UserRepository
            stub = Achievements_pb2_grpc.AchievementsControllerStub(channel)
            request = Achievements_pb2.GetAchievementListRequest(user_name=user_name)
            response = stub.GetAchivementList(request)

            # Convert achievements to JSON-serializable format
            achievements = [
                {
                    "title": achievement.title,
                    "description": achievement.description,
                    "date": achievement.date,
                    "rarity": achievement.rarity,
                }
                for achievement in response.achievements
            ]

            return {"achievements": achievements}
    except grpc.RpcError as e:
        return {"error": f"RPC failed: {e}"}, 500
    
def get_user_achievement(user_name, title):
    try:
        with grpc.insecure_channel('localhost:50080') as channel:  # Connect to the UserRepository
            stub = Achievements_pb2_grpc.AchievementsControllerStub(channel)
            request = Achievements_pb2.GetAchievementRequest(user_name=user_name, title=title)
            response = stub.GetAchievement(request)

            # Convert achievement to JSON-serializable format
            achievement = {
                "title": response.achievement.title,
                "description": response.achievement.description,
                "date": response.achievement.date,
                "rarity": response.achievement.rarity,
            }

            return {"achievement": achievement}
    except grpc.RpcError as e:
        return {"error": f"RPC failed: {e}"}, 500


def get_user_feed(user_name):
    try:
        with grpc.insecure_channel('localhost:50094') as channel:  # Connect to the FeedGenerator
            stub = FeedGenerator_pb2_grpc.FeedGeneratorServiceStub(channel)
            request = FeedGenerator_pb2.FeedRequest(user_name=user_name)
            print("aaaaa")
            response = stub.GetFeed(request)
            print("bbbbbbbbbb")

            print("publication: ", response.feed[0].name)

            # Convert feed to JSON-serializable format
            feed = [
                {
                    "name": publication.name,
                    "topic_name": publication.topicname,
                        "message": {
                            "username": publication.message.username,
                            "content": publication.message.content
                        },
                        "images": {
                            "name": publication.images.name,
                            "username": publication.images.username
                        }
                }
                for publication in response.feed
            ]

            return {"feed": feed}
    except grpc.RpcError as e:
        return {"error": f"RPC failed: {e}"}, 500
    
def get_user_topic_feed(user_name):
    try:
        with grpc.insecure_channel('localhost:50094') as channel:  # Connect to the FeedGenerator
            stub = FeedGenerator_pb2_grpc.FeedGeneratorServiceStub(channel)
            request = FeedGenerator_pb2.TopicFeedRequest(user_name=user_name)
            response = stub.GetTopicFeed(request)

            # Convert topic feed to JSON-serializable format
            topic_feed = [
                {
                "name": topic.topicname,
                "subscribers": [
                    {
                        "name": subscriber.name
                    }
                    for subscriber in topic.subscribers
                ],
                "publications": [
                    {
                        "name": publication.name,
                        "topic_name": publication.topicname,
                        "message": {
                            "username": publication.message.username,
                            "content": publication.message.content
                        },
                        "images": {
                            "name": publication.images.name,
                            "username": publication.images.username
                        }
                    }
                    for publication in topic.publications
                ]
                }
                for topic in response.topic_feed
            ]

            return {"topic_feed": topic_feed}
    except grpc.RpcError as e:
        return {"error": f"RPC failed: {e}"}, 500


if __name__ == "__main__":
    connex_app.run(host="0.0.0.0", port=50040)
