import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from python.others.AnimeList.AnimeList_pb2_grpc import (
    AnimeListServicer,
    add_AnimeListServicer_to_server,
)
from python.others.AnimeList.AnimeList_pb2 import (
    user_watched_anime_Response,
    anime_related_by_genre_Response,
)

from python.Common.Anime_pb2 import (
    Anime,
    AnimeGenre,
)

from python.services.Anime import AnimeService_pb2
from python.services.Anime import AnimeService_pb2_grpc

class AnimeList_Service(AnimeListServicer):

    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50053')  # Create a channel to the AnimeRepository
        self.stub = AnimeService_pb2_grpc.AnimeServiceStub(self.channel)

    def GetAllAnimes(self, request, context):
        return NotFound("Not implemented yet")
    
    def GetAnimeByName(self, request, context):
        return NotFound("Not implemented yet")
    
    def GetMultipleAnimeByName(self, request, context):
        return NotFound("Not implemented yet")

    def GetSimilarAnime(self, request, context):
        try:
            # Get the Anime objects from the AnimeService
            response_getAnime = self.stub.GetAnimeByName(AnimeService_pb2.anime_by_name_Request(anime_name=request.anime_name))
            anime = response_getAnime.anime

            # Get combination of genres related to the anime
            genres_conbinations = []
            # TODO: create a method to get combination of genres of an anime

            # Get animes related by genre
            animeList = []
            for genres in genres_conbinations:
                response = self.stub.GetAnimeByGenre(AnimeService_pb2.anime_by_genre_Request(anime_genre=genres))
                for anime in response.animes:
                    animeList.append(anime)
            return anime_related_by_genre_Response(animes=animeList)

        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))


    # ==================== auxiliary methods ====================

    # get combination of genres of an anime
    def get_combination_of_genres(self, anime_genres):
        # TODO: Finish this method
        return []

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