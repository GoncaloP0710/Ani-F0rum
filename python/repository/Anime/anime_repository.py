import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from python.repository.Anime.AnimeRepository_pb2_grpc import (
    AnimeRepositoryServicer,
    add_AnimeRepositoryServicer_to_server,
)
from python.repository.Anime.AnimeRepository_pb2 import (
    anime_by_genre_Response,
    anime_by_name_Response,
    get_animes_Response,
)

from python.Common.Anime_pb2 import (
    Anime,
    AnimeGenre,
)

class AnimeRepository_Service(AnimeRepositoryServicer) : 

    # TODO: Implement database connection and queries to retrieve anime data

    # Returns all animes of the given genre
    # TODO: Change it to recive a list of genres
    def GetAnimeRelatedByGenre(self, request, context):
        AnimeGenre = request.anime_genre
        print("Searching for anime with genre: ", AnimeGenre)
        return anime_by_genre_Response(animes=[])

    # Returns all animes
    def GetAnimes(self, request, context):
        print("Searching for all animes")
        return get_animes_Response(animes=[])
    
    # Returns an anime by name
    def GetAnimeByName(self, request, context):
        AnimeName = request.anime_name
        print("Searching for anime with name: ", AnimeName)
        # Create an Anime object TODO: Remove this part after testing
        anime = Anime(
            name="Naruto",
            genres=[AnimeGenre.ACTION, AnimeGenre.ADVENTURE],  # Example genres
            episodes=220,
            score=8.5,
            aired="2002-2007",
            synopsis="A young ninja strives to become the Hokage."
        )
        return anime_by_name_Response(anime=anime)
    

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_AnimeRepositoryServicer_to_server(
        AnimeRepository_Service(), server
    )
    server.add_insecure_port('[::]:50053')
    server.start()
    print("AnimeRepository Server started on port 50053")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
