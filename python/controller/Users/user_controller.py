import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import connexion
import pathlib

basedir = pathlib.Path(__file__).parent.resolve()

print(basedir)

connex_app = connexion.App(__name__, specification_dir=basedir)
connex_app.add_api(basedir / "swagger.yml")

import grpc
from python.others.UserRecommendations import UserRecommendations_pb2_grpc, UserRecommendations_pb2
from python.others.AnimeList import AnimeList_pb2_grpc, AnimeList_pb2
from python.Common import User_pb2 as Common_dot_User__pb2

def users_related_by_anime(user_name):

    # ============== Get the names of the animes watched by the user ==============
    # TODO: Right now we have a hardcoded list of animes watched by the user but once the GetUserByName exists we should call it and get the animes watched
    animes_name_watched=["Naruto","One Piece"]

    # ============== Get the animes watched by the user ==============
    animes_watched = []
    with grpc.insecure_channel('localhost:50052') as channel:  # Connect to the anime_list server
        stub = AnimeList_pb2_grpc.AnimeListStub(channel)
        request = AnimeList_pb2.get_multiple_anime_by_name_Request(anime_names=animes_name_watched)  # Create a request
        
        try:  # Make the request
            response = stub.GetMultipleAnimeByName(request)
            animes_watched = response.animes
        except grpc.RpcError as e:
            return {"error": f"RPC failed: {e}"}, 500
        
    # ============== Get the similar animes ==============
    similar_animes = []
    with grpc.insecure_channel('localhost:50052') as channel:  # Connect to the anime_list server
        stub = AnimeList_pb2_grpc.AnimeListStub(channel)
        for anime in animes_name_watched:
            request = AnimeList_pb2.get_similar_anime_Request(anime_name=anime)  # Create a request
            
            try:  # Make the request
                response = stub.GetSimilarAnime(request)
                similar_animes += response.animes
            except grpc.RpcError as e:
                return {"error": f"RPC failed: {e}"}, 500
            
    # remove multiple instances of the same anime
    similar_animes = list(set(similar_animes))

    # ============== Get the users related by anime ==============
    users_related_by_anime = []
    with grpc.insecure_channel('localhost:50042') as channel:  # Connect to the user_recommendations server
        stub = UserRecommendations_pb2_grpc.UserRecommendationsStub(channel)
        request = UserRecommendations_pb2.users_related_by_anime_Request(animes_watched=animes_watched,animes_similar=similar_animes)  # Create a request
        
        try:
            response = stub.GetUsersRelatedByAnime(request, None)
            users_related_by_anime = response.users
        except Exception as e:
            print(f"Error during test: {e}")
    
    # TODO: Verify return type
    return users_related_by_anime

if __name__ == "__main__":
    connex_app.run(host="0.0.0.0", port=50041)