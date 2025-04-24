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
client = bigquery.Client(project="cn-fc58192", location="europe-west1")

logging.basicConfig(
    level=logging.INFO,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.StreamHandler()  # Output logs to the console
    ]
)
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
        logging.info("Searching for user with id: %s", request.user_name)

        # Query user details
        query = "SELECT * FROM `cn-fc58192.vmcloud.users-details-2023` WHERE Username = @username"
        query_job = client.query(query, job_config=bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("username", "STRING", request.user_name)]
        ))
        result = list(query_job.result())  # Convert result to a list for easier handling
        logging.info("User details query result: %s", result)

        # Query user karma
        query = "SELECT * FROM `cn-fc58192.vmcloud.user-karma` WHERE user_name = @username"
        query_job = client.query(query, job_config=bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("username", "STRING", request.user_name)]
        ))
        result2 = list(query_job.result())  # Convert result to a list for easier handling
        logging.info("User karma query result: %s", result2)

        # Query user achievements
        query = "SELECT * FROM `cn-fc58192.vmcloud.user-achievements` WHERE user_name = @username"
        query_job = client.query(query, job_config=bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("username", "STRING", request.user_name)]
        ))
        result3 = list(query_job.result())  # Convert result to a list for easier handling
        logging.info("User achievements query result: %s", result3)

        # Query to get user anime watched and score
        query = "SELECT * FROM `cn-fc58192.vmcloud.users-score-2023` WHERE Username = @username"
        query_job = client.query(query, job_config=bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("username", "STRING", request.user_name)]
        ))
        result4 = list(query_job.result())  # Convert result to a list for easier handling
        logging.info("User anime watched and score query result: %s", result4)

        if not result:
            logging.info("User not found")
            raise NotFound("User not found")
        else:
            # Map the database result to the User object
            user_data = result[0]
            user_karma = result2[0] if result2 else None  # Get karma data if available
            user_achievements = [
                Achievement(
                    title=achievement["title"],
                    description=achievement["description"],
                    date=achievement["date"],
                    rarity=Rarity.Value(achievement["rarity"])
                )
                for achievement in result3  # Iterate over the list of achievements from the DB
            ] if result3 else []  # Default to empty list if no achievements
            animes_watched = [entry["Anime Title"] for entry in result4]  # Extract anime titles
            anime_watched_score = [entry["rating"] for entry in result4]  # Extract anime scores

            logging.info("User found: %s", user_data)

            # Extract fields from the database result
            user = User(
                user_name=user_data["Username"],  
                password="123",  
                location=user_data["Location"],  
                animes_watched=animes_watched,  
                anime_watched_score=anime_watched_score,  
                topics_subscribed=[], 
                karma=user_karma["karma"] if user_karma else 0, 
                achievements=user_achievements, 
            )

            return get_user_Response(user=user)
        
    # Returns all users
    def GetAllUsers(self, request, context):
        logging.info("Fetching all users")

        # Query to get all user details
        query = "SELECT * FROM `cn-fc58192.vmcloud.users-details-2023` LIMIT 10"
        query_job = client.query(query)
        user_details = list(query_job.result())  # Convert result to a list for easier handling
        logging.info("All user details query result: %s", user_details)

        # Query to get all user karma
        query = "SELECT * FROM `cn-fc58192.vmcloud.user-karma`"
        query_job = client.query(query)
        user_karma = {entry["user_name"]: entry["karma"] for entry in query_job.result()}  # Map user_name to karma
        logging.info("All user karma query result: %s", user_karma)

        # Query to get all user achievements
        query = "SELECT * FROM `cn-fc58192.vmcloud.user-achievements`"
        query_job = client.query(query)
        user_achievements = {}
        for entry in query_job.result():
            user_name = entry["user_name"]
            if user_name not in user_achievements:
                user_achievements[user_name] = []
            user_achievements[user_name].append(
                Achievement(
                    title=entry["title"],
                    description=entry["description"],
                    date=entry["date"],
                    rarity=Rarity.Value(entry["rarity"])
                )
            )
        logging.info("All user achievements query result: %s", user_achievements)

        # Query to get all user anime watched and scores
        query = "SELECT * FROM `cn-fc58192.vmcloud.users-score-2023`"
        query_job = client.query(query)
        user_anime = {}
        for entry in query_job.result():
            user_name = entry["Username"]
            if user_name not in user_anime:
                user_anime[user_name] = {"animes_watched": [], "anime_watched_score": []}
            user_anime[user_name]["animes_watched"].append(entry["anime_title"])
            user_anime[user_name]["anime_watched_score"].append(entry["rating"])
        logging.info("All user anime watched and score query result: %s", user_anime)

        # Map all users to User objects
        users = []
        for user_data in user_details:
            user_name = user_data["Username"]
            users.append(
                User(
                    user_name=user_name,
                    password="",  # Passwords are not retrieved for security reasons
                    location=user_data["Location"],
                    animes_watched=user_anime.get(user_name, {}).get("animes_watched", []),
                    anime_watched_score=user_anime.get(user_name, {}).get("anime_watched_score", []),
                    topics_subscribed=[],  # Add if available in the database
                    karma=user_karma.get(user_name, 0),
                    achievements=user_achievements.get(user_name, [])
                )
            )

        return get_all_users_Response(users=users)
    
    # Returns all users with one of the animes in their list
    def GetUsersThatWatchedAnime(self, request, context):
        logging.info("Searching for users that watched these animes: %s", request.anime_names)

        # Query to get usernames of users who watched the given anime(s)
        query = """
            SELECT DISTINCT Username 
            FROM `cn-fc58192.vmcloud.users-score-2023`
            WHERE `Anime Title` IN UNNEST(@anime_titles)
            LIMIT 10
        """
        query_job = client.query(query, job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ArrayQueryParameter("anime_titles", "STRING", request.anime_names)
            ]
        ))
        result = list(query_job.result())  # Convert result to a list for easier handling
        logging.info("Query result for users that watched the given animes: %s", result)

        # Retrieve full user objects using GetUser
        users = []
        for entry in result:
            username = entry["Username"]
            try:
                # Create a mock request to call GetUser
                user_request = type('Request', (object,), {"user_name": username})()
                user_response = self.GetUser(user_request, context)
                users.append(user_response.user)
            except NotFound:
                logging.warning("User not found for username: %s", username)

        logging.info("Found users: %s", users)
        return get_users_that_watched_anime_Response(users=users)
    #name
    def GetUserAchievements(self, request, context):
        logging.info("Searching for achievements of user: ", request.user_name)

        # Query user achievements
        query = "SELECT * FROM `cn-fc58192.vmcloud.user-achievements` WHERE user_name = @username"
        query_job = client.query(query, job_config=bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("username", "STRING", request.user_name)]
        ))
        result = list(query_job.result())  # Convert result to a list for easier handling
        logging.info("User achievements query result: %s", result)

        user_achievements = [
                Achievement(
                    title=achievement["title"],
                    description=achievement["description"],
                    date=achievement["date"],
                    rarity=Rarity.Value(achievement["rarity"])
                )
                for achievement in result  # Iterate over the list of achievements from the DB
            ] if result else []

        return get_user_achievements_Response(achievements=user_achievements)
        
    def GetAchievement(self, request, context):
        logging.info("Searching for achievement with title: ", request.title)
        
        # Query user achievements
        query = "SELECT * FROM `cn-fc58192.vmcloud.user-achievements` WHERE title = @title"
        query_job = client.query(query, job_config=bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("title", "STRING", request.title)]
        ))
        result = list(query_job.result())  # Convert result to a list for easier handling
        logging.info("Achievement title query result: %s", result)

        achievement = Achievement(
            title=result[0]["title"],
            description=result[0]["description"],
            date=result[0]["date"],
            rarity=Rarity.Value(result[0]["rarity"])
        ) if result else None

        return get_achievement_Response(achievement=achievement)
    
    def UpdateUserAchievement(self, request, context):
        logging.info("Updating user with user_name: %s and with title: %s", request.user_name, request.title)

        # Verificar se o achievement existe na tabela para o usuário
        query_check = """
            SELECT COUNT(*) as count
            FROM `cn-fc58192.vmcloud.user-achievements`
            WHERE user_name = @user_name AND title = @title
        """
        query_job = client.query(query_check, job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("user_name", "STRING", request.user_name),
                bigquery.ScalarQueryParameter("title", "STRING", request.title)
            ]
        ))
        result = list(query_job.result())
        achievement_exists = result[0]["count"] > 0

        if achievement_exists:
            logging.info("Achievement already exists for user: %s with title: %s", request.user_name, request.title)
            return update_user_achievement_Response(success=False, message="Achievement already exists")

        # Buscar o achievement na lista local
        ach = None
        for achievement in self.Achievements:
            if achievement.title == request.title:
                ach = achievement
                break

        if not ach:
            raise NotFound("Achievement not found")

        # Inserir o achievement na tabela
        query_insert = """
            INSERT INTO `cn-fc58192.vmcloud.user-achievements` (user_name, title, description, date, rarity)
            VALUES (@user_name, @title, @description, @date, @rarity)
        """
        query_job = client.query(query_insert, job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("user_name", "STRING", request.user_name),
                bigquery.ScalarQueryParameter("title", "STRING", ach.title),
                bigquery.ScalarQueryParameter("description", "STRING", ach.description),
                bigquery.ScalarQueryParameter("date", "STRING", ach.date),
                bigquery.ScalarQueryParameter("rarity", "STRING", ach.rarity.name)  # Convert enum to string
            ]
        ))

        try:
            query_job.result()  # Aguarda a execução da query
            logging.info("Achievement successfully added for user: %s with title: %s", request.user_name, request.title)
            return update_user_achievement_Response(success=True)
        except Exception as e:
            logging.error("Failed to add achievement for user: %s with title: %s. Error: %s", request.user_name, request.title, str(e))
            return update_user_achievement_Response(success=False, message="Failed to add achievement")
        
    def UpdateUserKarma(self, request, context):
        logging.info("Updating karma for user: %s by value: %d", request.user_name, request.karma_value)

        query = """
            DECLARE user_exists INT64;

            -- Verificar se o usuário já existe na tabela
            SET user_exists = (
                SELECT COUNT(*) 
                FROM `cn-fc58192.vmcloud.user-karma`
                WHERE user_name = @user_name
            );

            -- Se o usuário existir, atualize o karma
            IF user_exists > 0 THEN
                UPDATE `cn-fc58192.vmcloud.user-karma`
                SET karma = karma + @karma_value
                WHERE user_name = @user_name;
            ELSE
                -- Caso contrário, insira um novo registro
                INSERT INTO `cn-fc58192.vmcloud.user-karma` (user_name, karma)
                VALUES (@user_name, @karma_value);
            END IF;
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("user_name", "STRING", request.user_name),
                bigquery.ScalarQueryParameter("karma_value", "INT64", request.karma_value)
            ]
        )

        try:
            query_job = client.query(query, job_config=job_config)
            query_job.result()  # Aguarda a execução da query
            logging.info("Successfully updated or inserted karma for user: %s", request.user_name)
            return update_user_karma_Response(success=True)
        except Exception as e:
            logging.error("Failed to update or insert karma for user: %s. Error: %s", request.user_name, str(e))
            return update_user_karma_Response(success=False, message="Failed to update or insert karma")
    
    # def UpdateUserKarma(self, request, context):
    #     logging.info("Updating karma for user: %s by value: %d", request.user_name, request.karma_value)

    #     # Verificar se o usuário existe na tabela
    #     query_check = """
    #         SELECT COUNT(*) as count
    #         FROM `cn-fc58192.vmcloud.user-karma`
    #         WHERE user_name = @user_name
    #     """
    #     query_job = client.query(query_check, job_config=bigquery.QueryJobConfig(
    #         query_parameters=[
    #             bigquery.ScalarQueryParameter("user_name", "STRING", request.user_name)
    #         ]
    #     ))
    #     result = list(query_job.result())
    #     user_exists = result[0]["count"] > 0

    #     if user_exists:
    #         # Atualizar o karma do usuário existente
    #         query_update = """
    #             UPDATE `cn-fc58192.vmcloud.user-karma`
    #             SET karma = karma + @karma_value
    #             WHERE user_name = @user_name
    #         """
    #         query_job = client.query(query_update, job_config=bigquery.QueryJobConfig(
    #             query_parameters=[
    #                 bigquery.ScalarQueryParameter("user_name", "STRING", request.user_name),
    #                 bigquery.ScalarQueryParameter("karma_value", "INT64", request.karma_value)
    #             ]
    #         ))
    #     else:
    #         # Inserir um novo registro para o usuário
    #         query_insert = """
    #             INSERT INTO `cn-fc58192.vmcloud.user-karma` (user_name, karma)
    #             VALUES (@user_name, @karma_value)
    #         """
    #         query_job = client.query(query_insert, job_config=bigquery.QueryJobConfig(
    #             query_parameters=[
    #                 bigquery.ScalarQueryParameter("user_name", "STRING", request.user_name),
    #                 bigquery.ScalarQueryParameter("karma_value", "INT64", request.karma_value)
    #             ]
    #         ))

    #     try:
    #         query_job.result()  # Aguarda a execução da query
    #         logging.info("Successfully updated or inserted karma for user: %s", request.user_name)
    #         return update_user_karma_Response(success=True)
    #     except Exception as e:
    #         logging.error("Failed to update or insert karma for user: %s. Error: %s", request.user_name, str(e))
    #         return update_user_karma_Response(success=False, message="Failed to update or insert karma")
        
    

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
