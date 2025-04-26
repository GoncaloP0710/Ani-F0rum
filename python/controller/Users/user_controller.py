import logging
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
    print("Top 10 Response:", top10_response)  # Debugging line
    animes_name_watched = [anime['name'] for anime in top10_response['top10_anime']]
    animes_watched = []
    similar_animes = []

    try:
        with grpc.insecure_channel('anime-list:50052') as channel:
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

        with grpc.insecure_channel('user-recommendations:50042') as channel:
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
    logging.info("getting all users")
    try:
        with grpc.insecure_channel('user-statistics:50041') as channel:
            stub = UserStatistics_pb2_grpc.UserStatisticsServiceStub(channel)
            request = UserStatistics_pb2.Empty()
            logging.info("request built")
            response = stub.GetAllUsers(request)
            logging.info("response")
            logging.info(response)
            return {
                "users": [
                    {
                        "user_name": user.user_name,
                        "password": user.password,
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
        with grpc.insecure_channel('user-statistics:50041') as channel:
            stub = UserStatistics_pb2_grpc.UserStatisticsServiceStub(channel)
            request = UserStatistics_pb2.GetUserByNameRequest(user_name=user_name)
            response = stub.GetUserByName(request)
            user = response.user
            return {
                "user": {
                    "user_name": user.user_name,
                    "password": user.password,
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
        with grpc.insecure_channel('user-statistics:50041') as channel:
            stub = UserStatistics_pb2_grpc.UserStatisticsServiceStub(channel)
            request = UserStatistics_pb2.KarmaRequest(user_name=user_name)
            response = stub.GetUserKarma(request)
            return {"karma": response.karma_Value}
    except grpc.RpcError as e:
        return {"error": f"RPC failed: {e}"}, 500


def top10Anime(user_name):
    try:
        with grpc.insecure_channel('user-statistics:50041') as channel:
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
        with grpc.insecure_channel('user-statistics:50041') as channel:
            stub = UserStatistics_pb2_grpc.UserStatisticsServiceStub(channel)
            request = UserStatistics_pb2.MostUsedTopics_Request(user_name=user_name)
            response = stub.GetMostUsedTopics(request)

            topics_list = [
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
                for topic in response.most_used_topics
            ]
            return {"topics": topics_list}
    except grpc.RpcError as e:
        return {"error": f"RPC failed: {e}"}, 500

def GetAchivementList(user_name):
    try:
        with grpc.insecure_channel('achievements:50080') as channel:  
            stub = Achievements_pb2_grpc.AchievementsControllerStub(channel)
            request = Achievements_pb2.AchievementListRequest(user_name=user_name)
            print(request)
            response = stub.GetAchivementList(request)
            achievements = response.achievements

            if not achievements:
                return {"error": "User not found"}, 404

            # Convert achievements to JSON-serializable format
            achievement_list = [
                {
                    "title": achievement.title,
                    "description": achievement.description,
                    "date": achievement.date,
                    "rarity": achievement.rarity,
                }
                for achievement in achievements
            ]

            return {"achievements": achievement_list}
    except grpc.RpcError as e:
        return {"error": f"RPC failed: {e}"}, 500


def GetAchievement(title):
    try:
        with grpc.insecure_channel('achievements:50080') as channel:  
            stub = Achievements_pb2_grpc.AchievementsControllerStub(channel)
            request = Achievements_pb2.AchievementRequest(title=title)
            print(request)
            response = stub.GetAchievement(request)
            achievement = response.item

            if not achievement:
                return {"error": "Achievement not found"}, 404

            # Convert achievement to JSON-serializable format
            achievement_data = {
                "title": achievement.title,
                "description": achievement.description,
                "date": achievement.date,
                "rarity": achievement.rarity,
            }

            return {"achievement": achievement_data}
    except grpc.RpcError as e:
        return {"error": f"RPC failed: {e}"}, 500

def UpdateAchievement(user_name, title):
    try:
        with grpc.insecure_channel('achievements:50080') as channel: 
            stub = Achievements_pb2_grpc.AchievementsControllerStub(channel)
            request = Achievements_pb2.UpdateRequest(user_name=user_name, title=title)
            print(request)
            response = stub.UpdateAchievement(request)

            if not response.success:
                return {"error": "Failed to update achievement"}, 500

            if(response.success):
                return {"message": "Achievement updated successfully"}
            else:
                return {"message": "Unable to update achievement"}
    except grpc.RpcError as e:
        return {"error": f"RPC failed: {e}"}, 500
    


def get_user_feed(user_name):
    try:
        with grpc.insecure_channel('feed-generator:50094') as channel:  # Connect to the FeedGenerator
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
        with grpc.insecure_channel('feed-generator:50094') as channel:  # Connect to the FeedGenerator
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
    
def update_user_karma(user_name, karma_value):
    try:
        # Convert karma_value to an integer
        karma_value = int(karma_value)

        with grpc.insecure_channel('user-statistics:50041') as channel:
            stub = UserStatistics_pb2_grpc.UserStatisticsServiceStub(channel)
            
            request = UserStatistics_pb2.KarmaUpdateRequest(user_name=user_name, karma_value=karma_value)
            
            response = stub.UpdateUserKarma(request)
            
            return {"success": response.success}
    except ValueError as ve:
        logging.error(f"ValueError: karma_value must be an integer. Error: {ve}")
        return {"error": "karma_value must be an integer"}, 400
    except grpc.RpcError as e:
        logging.error(f"gRPC error occurred: {e}")
        return {"error": f"RPC failed: {e}"}, 500
    except Exception as ex:
        logging.error(f"Unexpected error occurred: {ex}")
        return {"error": "Internal server error"}, 500


def healthz():
    return {"status": "ok"}, 200

def readiness():
    return {"status": "ready"}, 200

def startup():
    return {"status": "started"}, 200

if __name__ == "__main__":
    connex_app.run(host="0.0.0.0", port=50040)
