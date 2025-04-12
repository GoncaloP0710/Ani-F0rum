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
from python.others.AnimeList import AnimeList_pb2_grpc, AnimeList_pb2
from python.Common import User_pb2 as Common_dot_User__pb2
from python.others.UserStatistics import UserStatistics_pb2_grpc, UserStatistics_pb2

def all_anime():
    with grpc.insecure_channel('anime-list:50052') as channel:  # Connect to the anime_list server
        stub = AnimeList_pb2_grpc.AnimeListStub(channel)
        request = AnimeList_pb2.get_all_animes()  # Create a request
        
        try:  # Make the request
            response = stub.GetAllAnimes(request)
            # Convert Anime objects to JSON-serializable dictionaries
            return [
                {
                    "name": anime.name,
                    "genres": list(anime.genres),  # Convert genres to a list
                    "episodes": anime.episodes,
                    "score": anime.score,
                    "aired": anime.aired,
                    "synopsis": anime.synopsis,
                }
                for anime in response.animes
            ]
        except grpc.RpcError as e:
            return {"error": f"RPC failed: {e}"}, 500
        
def get_anime(anime_name):

    print("===================== Get Anime ====================")
    print (anime_name)

    with grpc.insecure_channel('anime-list:50052') as channel:  # Connect to the anime_list server
        stub = AnimeList_pb2_grpc.AnimeListStub(channel)
        request = AnimeList_pb2.get_anime_by_name_Request(anime_name=anime_name)  # Create a request
        
        try:  # Make the request
            response = stub.GetAnimeByName(request)
            return {
                "name": response.anime.name,
                "genres": list(response.anime.genres),  # Convert genres to a list
                "episodes": response.anime.episodes,
                "score": response.anime.score,
                "aired": response.anime.aired,
                "synopsis": response.anime.synopsis,
            }
        except grpc.RpcError as e:
            return {"error": f"RPC failed: {e}"}, 500
        
def get_similar_anime(anime_name):
    with grpc.insecure_channel('anime-list:50052') as channel:  # Connect to the anime_list server
        stub = AnimeList_pb2_grpc.AnimeListStub(channel)
        request = AnimeList_pb2.get_similar_anime_Request(anime_name=anime_name)  # Create a request
        
        try:  # Make the request
            response = stub.GetSimilarAnime(request)
            return [
                {
                    "name": anime.name,
                    "genres": list(anime.genres),  # Convert genres to a list
                    "episodes": anime.episodes,
                    "score": anime.score,
                    "aired": anime.aired,
                    "synopsis": anime.synopsis,
                }
                for anime in response.animes
            ] 
        except grpc.RpcError as e:
            return {"error": f"RPC failed: {e}"}, 500

def get_similar_anime_list(user_name):
    top10_anime = None
    with grpc.insecure_channel('localhost:50060') as channel:
        stub = UserStatistics_pb2_grpc.UserStatisticsServiceStub(channel)
        request = UserStatistics_pb2.Top10_Request(user_name=user_name)
        try:
            response = stub.GetTop10(request)
            print("===================== Get Top 10 Anime ====================")
            print(response)
            # Extract only the names of the top 10 anime
            top10_anime = response.animes
        except grpc.RpcError as e:
            return {"error": f"RPC failed: {e}"}, 500

    print("===================== Get Similar Anime List ====================")
    print(top10_anime)
    
    with grpc.insecure_channel('anime-list:50052') as channel:
        stub = AnimeList_pb2_grpc.AnimeListStub(channel)
        request = AnimeList_pb2.recomended_animeList_Request(animes_most_liked=top10_anime)

        try:
            response = stub.GetRecomendedAnimeList(request)
            return [
                {
                    "name": anime.name,
                    "genres": list(anime.genres),  # Convert genres to a list
                    "episodes": anime.episodes,
                    "score": anime.score,
                    "aired": anime.aired,
                    "synopsis": anime.synopsis,
                }
                for anime in response.animes
            ]
        except grpc.RpcError as e:
            return {"error": f"RPC failed: {e}"}, 500  # Add this block to handle exceptions

if __name__ == "__main__":
    connex_app.run(host="0.0.0.0", port=50051)


