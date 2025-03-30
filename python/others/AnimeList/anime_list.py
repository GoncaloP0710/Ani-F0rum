import random
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
    recomended_animeList_Response,
    get_similar_anime_Request,
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
            print (response)
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
            # Call the AnimeRepository service
            response = self.stub.MultipleAnimeByName(
                AnimeRepository_pb2.multiple_anime_by_name_Request(anime_names=request.anime_names)
            )
            # Use the correct field name "animes"
            return get_multiple_anime_by_name_Response(animes=response.animes)
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
            animeList = []  # Use a list instead of a set
            for genres in genres_conbinations:
                response = self.stub.AnimeRelatedByGenre(
                    AnimeRepository_pb2.anime_by_genre_Request(anime_genres=genres)
                )
                for anime in response.animes:
                    animeList.append(anime)  # Add anime to the list

            # Remove duplicates by using a dictionary with the anime name as the key
            animeList = list({anime.name: anime for anime in animeList}.values())

            # Randomize the selection, limiting to 5 elements
            if len(animeList) > 5:
                animeList = random.sample(animeList, 5)  # Randomly select 10 elements

            return get_similar_anime_Response(animes=animeList)

        
        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))

    # Used when user wants to get animes recommended to him based on his watched animes and the rankings he gave them
    # It should be called after getting the most liked animes by the user
    # TODO: Try the method once the getter for the most liked animes by the user is 100% functional
    def GetRecomendedAnimeList(self, request, context):
        try:
            animes_recommendation = []  # Use a list instead of a set

            # Loop through the most liked animes
            for anime in request.animes_most_liked:
                # Call GetSimilarAnime for each anime
                similar_anime_response = self.GetSimilarAnime(
                    get_similar_anime_Request(anime_name=[anime.name]),
                    context
                )
                for similar_anime in similar_anime_response.animes:
                    # Add anime to the list only if it's not already present
                    if similar_anime not in animes_recommendation:
                        animes_recommendation.append(similar_anime)

            # Randomize the selection, limiting to 15 elements
            if len(animes_recommendation) > 15:
                animes_recommendation = random.sample(animes_recommendation, 15)  # Randomly select 15 elements

            # Return the response
            return recomended_animeList_Response(animes=animes_recommendation)

        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
            

    # ==================== auxiliary methods ====================

    # get combination of genres of an anime
    @staticmethod
    def get_combination_of_genres(anime_genres):

        # Calculate the target size (60% of the original list size)
        target_size = max(1, int(len(anime_genres) * 0.8))  # Ensure at least 1 genre is included

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

    # Test functions
    print("===========================================")
    print ("Test GetAllAnimes")
    print (AnimeList_Service().GetAllAnimes(None, None))
    print("===========================================")

    print("===========================================")
    print ("Test GetAnimeByName")
    print (AnimeList_Service().GetAnimeByName(AnimeRepository_pb2.anime_by_name_Request(anime_name="Naruto"), None))
    print("===========================================")

    print("===========================================")
    print ("Test GetMultipleAnimeByName")
    print (AnimeList_Service().GetMultipleAnimeByName(AnimeRepository_pb2.multiple_anime_by_name_Request(anime_names=["Naruto", "One Piece"]), None))
    print("===========================================")

    print("===========================================")
    print ("Test GetSimilarAnime")
    print (AnimeList_Service().GetSimilarAnime(get_similar_anime_Request(anime_name="Naruto"), None))
    print("===========================================")

    server.wait_for_termination()

if __name__ == '__main__':
    serve()