import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from concurrent import futures

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
    # TODO: After testing, uncomment the following line
    # update_User_Response,
)

# TODO: Change that latter for the correct import
from python.Common.User_pb2 import (
    User,
    Achievement,
    Rarity,
)

class UserRepository_Service(UserRepositoryServicer) :

    # TODO: Implement database connection and queries to retrieve user database

    # Example list of users
    Users = [
        User(
            user_name="JohnDoe",
            password="password123",
            location="USA",
            animes_watched=["Naruto", "One Piece", "Attack on Titan"],
            anime_watched_score=[9, 10, 8],
            topics_subscribed=["Anime Discussions", "Manga Reviews"],
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
        )
    ]

    # Returns an user by name
    def GetUser(self, request, context):
        print("Searching for user with id: ", request.user_name)
        for user in self.Users:
            if user.user_name == request.user_name:
                return get_user_Response(user=user)
        raise NotFound("User not found")

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
    
    # TODO: Remove comments when _pb2_grpc files are updated
    # Returns success of the update
    #def UpdateUser(self, request, context):
    #    print("Updating user: ", request.user.user_name)
    #    return update_User_Response(success=bool())

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
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
