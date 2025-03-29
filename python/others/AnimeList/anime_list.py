import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from concurrent import futures
from itertools import combinations

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from python.others.AnimeList.AnimeList_pb2_grpc import (
    AnimeListServicer,
    add_AnimeListServicer_to_server,
)
from python.others.AnimeList.AnimeList_pb2 import (
    get_all_animes_Response,
    get_anime_by_name_Response,
    get_multiple_anime_by_name_Response,
    get_similar_anime_Response,
)

from python.Common.Anime_pb2 import (
    Anime,
    AnimeGenre,
) 

from python.repository.Anime import AnimeRepository_pb2
from python.repository.Anime import AnimeRepository_pb2_grpc

class AnimeList_Service(AnimeListServicer):

    # Create a channel and a stub to the AnimeRepository microservice so we can call its methods
    def __init__(self): 
        self.channel = grpc.insecure_channel('localhost:50053')  # Create a channel to the AnimeRepository
        self.stub = AnimeRepository_pb2_grpc.AnimeRepositoryStub(self.channel)

    # Used when user wants to list all animes
    def GetAllAnimes(self, request, context):
        try:
            response = self.stub.Animes(AnimeRepository_pb2.animes_Request())
            return get_all_animes_Response(animes=response.animes)
        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
    
    # Used when user wants to get all the information on a specific anime
    def GetAnimeByName(self, request, context):
        try:
            response = self.stub.AnimeByName(AnimeRepository_pb2.anime_by_name_Request(anime_name=request.anime_name))
            return get_anime_by_name_Response(anime=response.anime)
        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
    
    # Used when user wants to get all the information on multiple animes that he specifies
    def GetMultipleAnimeByName(self, request, context):
        try:
            response = self.stub.MultipleAnimeByName(AnimeRepository_pb2.multiple_anime_by_name_Request(anime_name=request.anime_name))
            return get_multiple_anime_by_name_Response(anime=response.animes)
        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))

    # Used when user wants to get animes similar to the one he specifies
    def GetSimilarAnime(self, request, context):
        try:
            # Get the Anime objects from the AnimeService
            response_getAnime = self.stub.AnimeByName(AnimeRepository_pb2.anime_by_name_Request(anime_name=request.anime_name))
            anime = response_getAnime.anime

            # Get combination of genres related to the anime
            genres_conbinations = self.get_combination_of_genres(anime.genres)

            # Get animes related by genre
            animeList = set()  # Use a set to avoid duplicates
            for genres in genres_conbinations:
                response = self.stub.GetAnimeByGenre(AnimeRepository_pb2.anime_by_genre_Request(anime_genre=genres))
                for anime in response.animes:
                    animeList.add(anime)  # Add anime to the set

            # Convert the set back to a list before returning
            return get_similar_anime_Response(animes=list(animeList))

        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))


    # ==================== auxiliary methods ====================

    # get combination of genres of an anime
    def get_combination_of_genres(anime_genres):
        # Calculate the target size (60% of the original list size)
        target_size = max(1, int(len(anime_genres) * 0.6))  # Ensure at least 1 genre is included

        # Get all possible combinations of genres
        genre_combinations = list(combinations(anime_genres, target_size))

        # Convert tuples to lists (if needed)
        return [list(combination) for combination in genre_combinations]

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_AnimeListServicer_to_server(
        AnimeList_Service(), server
    )
    server.add_insecure_port('[::]:50052')
    server.start()
    print('AnimeList server running on port 50052')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()