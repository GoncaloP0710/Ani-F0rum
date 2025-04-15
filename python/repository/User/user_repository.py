import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from concurrent import futures
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from python.repository.User.UserRepository_pb2_grpc import (
    UserRepositoryServicer,
    add_UserRepositoryServicer_to_server,
)
from python.repository.User.UserRepository_pb2 import (
    get_user_Response,
    get_all_users_Response,
    get_users_that_watched_anime_Response,
    get_achievement_Response,
    get_user_achievements_Response,
    update_user_achievement_Response,
    update_user_karma_Response,
    # TODO: After testing, uncomment the following line
    # update_User_Response,
)

# TODO: Change that latter for the correct import
from python.Common.User_pb2 import (
    User,
    Achievement,
    Rarity,
)
from flask import Flask, request, abort
from google.cloud import bigquery
#from google.oauth2 import service_account
import json, os
import logging

# json_string = os.environ.get("API_TOKEN")
# json_file = json.loads(json_string)
# credentials = service_account.Credentials.from_service_account_info(json_file)
client = bigquery.Client(location="europe-west1")

class UserRepository_Service(UserRepositoryServicer) :

    Achievements = [
        Achievement(
            title="Anime Enthusiast",
            description="Watched 100+ anime series",
            date="2025-03-26",
            rarity=Rarity.EPIC
        ),
        Achievement(
            title="Manga Collector",
            description="Collected 50+ manga volumes",
            date="2025-03-20",
            rarity=Rarity.RARE
        ),
        Achievement(
            title="Cosplay Champion",
            description="Won 5 cosplay competitions",
            date="2024-12-15",
            rarity=Rarity.LEGENDARY
        ),
        Achievement(
            title="Wow",
            description="Big win",
            date="2025-04-15",
            rarity=Rarity.LEGENDARY
        ),
        Achievement(
            title="Anime Historian",
            description="Watched anime from every decade since the 1980s",
            date="2025-01-10",
            rarity=Rarity.MYTHIC
        )
    ]
    # TODO: Implement database connection and queries to retrieve user database

    # Example list of users
    Users = [
        User(
            user_name="JohnDoe",
            password="password123",
            location="USA",
            animes_watched=["Naruto", "One Piece", "Attack on Titan"],
            anime_watched_score=[9, 10, 8],
            topics_subscribed=["Solo Leveling ep12", "Solo Leveling images"],
            karma=150,
            achievements=[
                Achievement(
                    title="Anime Enthusiast",
                    description="Watched 100+ anime series",
                    date="2025-03-26",
                    rarity=Rarity.EPIC
                ),
                Achievement(
                    title="Manga Collector",
                    description="Collected 50+ manga volumes",
                    date="2025-03-20",
                    rarity=Rarity.RARE
                )
            ]
        ),
        User(
            user_name="JaneSmith",
            password="securepass",
            location="UK",
            animes_watched=["Demon Slayer", "My Hero Academia", "Death Note"],
            anime_watched_score=[10, 9, 10],
            topics_subscribed=["Cosplay", "Anime Art"],
            karma=200,
            achievements=[
                Achievement(
                    title="Cosplay Champion",
                    description="Won 5 cosplay competitions",
                    date="2024-12-15",
                    rarity=Rarity.LEGENDARY
                )
            ]
        ),
        User(
            user_name="AnimeFan123",
            password="animeislife",
            location="Japan",
            animes_watched=["Dragon Ball", "Bleach", "Fullmetal Alchemist"],
            anime_watched_score=[8, 9, 10],
            topics_subscribed=["Anime News", "Fan Theories"],
            karma=300,
            achievements=[
                Achievement(
                    title="Anime Historian",
                    description="Watched anime from every decade since the 1980s",
                    date="2025-01-10",
                    rarity=Rarity.MYTHIC
                )
            ]
        ),
        User(
            user_name="Diogo",
            password="password123",
            location="Portugal",
            animes_watched=["Naruto", "One Piece", "Attack on Titan"],
            anime_watched_score=[9, 10, 8],
            topics_subscribed=["Solo Leveling ep12", "Solo Leveling images"],
            karma=150,
            achievements=[
                Achievement(
                    title="Anime Enthusiast",
                    description="Watched 100+ anime series",
                    date="2025-03-26",
                    rarity=Rarity.EPIC
                ),
                Achievement(
                    title="Manga Collector",
                    description="Collected 50+ manga volumes",
                    date="2025-03-20",
                    rarity=Rarity.RARE
                )
            ]
        ),
    ]

    # Returns an user by name
    def GetUser(self, request, context):
        print("Searching for user with id: ", request.user_name)
        #logging.info("Doing something important...")
        
        
       # return get_user_Response(user=self.Users[0])

        query = "SELECT * FROM cn-fc58192.vmcloud.users WHERE user_name =" + request.user_name 
        query_job = client.query(query)
        result = query_job.result()
        

        if not result:

            query = "SELECT * FROM cn-fc58192.vmcloud.animelist WHERE user_id =" + request.user_name 
            query_job = client.query(query)
            result = query_job.result()
            #criar user e insert em cn-fc58192.vmcloud.users

            if not result:
                raise NotFound("User not found")
            
            # user = User(
            #     user_name = result.user_id,
            #     password = "-",
            #     location = "-",
            #     animes_watched = result.anime_id,
            #     anime_watched_score = result.rating,
            #     topics_subscribed = ["default"],
            #     karma = 0,
            #     achievements = [Achievement(
            #         title="Anime Enthusiast",
            #         description="Watched 100+ anime series",
            #         date="2025-03-26",
            #         rarity=Rarity.EPIC
            #     ),]
            # )

            return get_user_Response(user=result)
            
            
        else:
           return get_user_Response(user=result)
        
        for user in self.Users:
            if user.user_name == request.user_name:
                return get_user_Response(user=user)
            

    # Returns all users
    def GetAllUsers(self, request, context):
        print("Searching for all users")
        return get_all_users_Response(users=self.Users)
    
    # Returns all users with one of the animes in their list
    def GetUsersThatWatchedAnime(self, request, context):
        print("Searching for users that watched these animes: ", request.anime_names)
        users = []  # Use a list instead of a set
        for anime in request.anime_names:
            for user in self.Users:
                if anime in user.animes_watched and user not in users:
                    users.append(user)  # Add user to the list if not already present

        print("Found users: ", users)
        return get_users_that_watched_anime_Response(users=users)
    name
    def GetUserAchievements(self, request, context):
        print("Searching for achievements of user: ", request.user_name)
        for user in self.Users:
            if user.user_name == request.user_name:
                return get_user_achievements_Response(achievements=user.achievements)
        raise NotFound("User not found")
        
    def GetAchievement(self, request, context):
        print("Searching for achievement with title: ", request.title)
        for achievement in self.Achievements:
            if achievement.title == request.title:
                return get_achievement_Response(achievement=achievement)
        raise NotFound("Achievement not found")
    
    def UpdateUserAchievement(self, request, context):
        print("Updating user with user_name: ", request.user_name," and with title: ", request.title)

        ach = None
        err = True
        for achievement in self.Achievements:
            if achievement.title == request.title:
                ach = achievement
                err = False
                break
        
        if err:
            raise NotFound("Achievement not found")

        for user in self.Users:
            if user.user_name == request.user_name:
                user.achievements.append(ach)
                return update_user_achievement_Response(success=True)
        
        return update_user_achievement_Response(success=False)
    
    def UpdateUserKarma(self, request, context):
        print("Updating karma of user: ", request.user_name)
        for user in self.Users:
            if user.user_name == request.user_name:
                user.karma += request.karma_value
                return update_user_karma_Response(success=True)
        
        return update_user_karma_Response(success=False)
        
    

    # TODO: Remove comments when _pb2_grpc files are updated
    # Returns success of the update
    #def UpdateUser(self, request, context):
    #    print("Updating user: ", request.user.user_name)
    #    return update_User_Response(success=bool())

# ----------------------------------------------------------------
# HTTP server for Kubernetes probes
class ProbeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/healthz", "/readiness", "/startup"]:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

def start_http_server():
    http_server = HTTPServer(('0.0.0.0', 8080), ProbeHandler)
    print("HTTP server for probes started on port 8080")
    http_server.serve_forever()
# ----------------------------------------------------------------

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_UserRepositoryServicer_to_server(
        UserRepository_Service(), server
    )
    server.add_insecure_port('[::]:50043')
    server.start()
    print("UserRepository server running on port 50043")
    
    # -------------------------------------------------
    # Start the HTTP server for probes in a separate thread
    http_thread = threading.Thread(target=start_http_server)
    http_thread.daemon = True
    http_thread.start()

    server.wait_for_termination()
    # --------------------------------------------------

if __name__ == '__main__':
    serve()
