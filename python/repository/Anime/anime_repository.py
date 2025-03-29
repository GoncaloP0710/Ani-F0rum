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

    Animes = [
        Anime(
            name="Naruto",
            genres=[AnimeGenre.ACTION, AnimeGenre.ADVENTURE],
            episodes=220,
            score=8.5,
            aired="2002-2007",
            synopsis="A young ninja strives to become the Hokage."
        ),
        Anime(
            name="One Piece",
            genres=[AnimeGenre.ACTION, AnimeGenre.ADVENTURE],
            episodes=1000,
            score=9.0,
            aired="1999-",
            synopsis="A young pirate strives to become the Pirate King."
        ),
        Anime(
            name="Dragon Ball",
            genres=[AnimeGenre.ACTION, AnimeGenre.ADVENTURE],
            episodes=153,
            score=8.5,
            aired="1986-1989",
            synopsis="A young warrior strives to become the strongest fighter."
        ),
    ]


    # Returns all animes
    def Animes(self, request, context):
        print("Searching for all animes")
        return get_animes_Response(animes=self.Animes)
    
    # Returns an anime by name
    def AnimeByName(self, request, context):
        AnimeName = request.anime_name
        print("Searching for anime with name: ", AnimeName)
        # Create an Anime object TODO: Remove this part after testing
        for anime in self.Animes:
            if anime.name == AnimeName:
                return anime_by_name_Response(anime=anime)
        raise NotFound("Anime not found")
    
    def MultipleAnimeByName(self, request, context):
        return NotFound("Not implemented yet")
    
    # Returns all animes that belong to some of the given genres
    def AnimeRelatedByGenre(self, request, context):
        return NotFound("Not implemented yet")
    

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
