import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import grpc
from python.others.AnimeList import AnimeList_pb2_grpc, AnimeList_pb2
from python.Common import User_pb2 as Common_dot_User__pb2

def run():
    # Connect to the anime_list server
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = AnimeList_pb2_grpc.AnimeListStub(channel)

        # Create a User object
        user = Common_dot_User__pb2.User(
            username="Gajo",
            password="securepassword",
            location="Portugal",
            animes_watched=["Naruto", "One Piece", "Attack on Titan"],
            anime_watched_score=[9, 10, 8],
            topics_subscribed=["Anime Discussions", "Manga Reviews"],
            karma=100,
            achievements=[
                Common_dot_User__pb2.Achievement(
                    title="Anime Enthusiast",
                    description="Watched 100+ anime series",
                    date="2025-03-26",
                    rarity=Common_dot_User__pb2.Rarity.EPIC
                ),
                Common_dot_User__pb2.Achievement(
                    title="Manga Collector",
                    description="Collected 50+ manga volumes",
                    date="2025-03-20",
                    rarity=Common_dot_User__pb2.Rarity.RARE
                )
            ]
        )        
        # Create a request
        request = AnimeList_pb2.user_watched_anime_Request(user = user)
        
        try:
            # Make the request
            response = stub.GetUserWatchedAnime(request)
            print(response)
        except grpc.RpcError as e:
            print(f"RPC failed: {e}")

if __name__ == '__main__':
    run()