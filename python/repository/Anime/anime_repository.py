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
    animes_Response,
    anime_by_name_Response,
    multiple_anime_by_name_Response,
    anime_by_genre_Response,
)

from python.Common.Anime_pb2 import (
    Anime,
    AnimeGenre,
)

class AnimeRepository_Service(AnimeRepositoryServicer) : 

    # TODO: Implement database connection and queries to retrieve anime data

    Animes_Objects = [
        Anime(
            name="Naruto",
            genres=[AnimeGenre.ACTION, AnimeGenre.ADVENTURE, AnimeGenre.DRAMA],
            episodes=220,
            score=8.5,
            aired="2002-2007",
            synopsis="A young ninja strives to become the Hokage."
        ),
        Anime(
            name="One Piece",
            genres=[AnimeGenre.ACTION, AnimeGenre.ADVENTURE, AnimeGenre.COMEDY],
            episodes=1000,
            score=9.0,
            aired="1999-present",
            synopsis="A young pirate strives to become the Pirate King."
        ),
        Anime(
            name="Dragon Ball",
            genres=[AnimeGenre.ACTION, AnimeGenre.ADVENTURE, AnimeGenre.FANTASY],
            episodes=153,
            score=8.5,
            aired="1986-1989",
            synopsis="A young warrior strives to become the strongest fighter."
        ),
        Anime(
            name="Attack on Titan",
            genres=[AnimeGenre.ACTION, AnimeGenre.THRILLER, AnimeGenre.DRAMA],
            episodes=75,
            score=9.2,
            aired="2013-present",
            synopsis="Humanity fights for survival against giant humanoid Titans."
        ),
        Anime(
            name="Demon Slayer",
            genres=[AnimeGenre.ACTION, AnimeGenre.FANTASY, AnimeGenre.DRAMA],
            episodes=26,
            score=8.7,
            aired="2019",
            synopsis="A young boy becomes a demon slayer to avenge his family."
        ),
        Anime(
            name="My Hero Academia",
            genres=[AnimeGenre.ACTION, AnimeGenre.ADVENTURE, AnimeGenre.COMEDY],
            episodes=113,
            score=8.6,
            aired="2016-present",
            synopsis="A boy born without superpowers in a world where they are common."
        ),
        Anime(
            name="Death Note",
            genres=[AnimeGenre.MYSTERY, AnimeGenre.THRILLER, AnimeGenre.DRAMA],
            episodes=37,
            score=9.0,
            aired="2006-2007",
            synopsis="A high school student discovers a supernatural notebook."
        ),
        Anime(
            name="Bleach",
            genres=[AnimeGenre.ACTION, AnimeGenre.ADVENTURE, AnimeGenre.FANTASY],
            episodes=366,
            score=8.1,
            aired="2004-2012",
            synopsis="A teenager becomes a Soul Reaper to protect the living and the dead."
        ),
        Anime(
            name="Fullmetal Alchemist: Brotherhood",
            genres=[AnimeGenre.ACTION, AnimeGenre.ADVENTURE, AnimeGenre.FANTASY],
            episodes=64,
            score=9.1,
            aired="2009-2010",
            synopsis="Two brothers use alchemy in their quest to restore their bodies."
        )
    ]

    # Returns all animes
    def Animes(self, request, context):
        print("Searching for all animes")
        return animes_Response(animes=self.Animes_Objects)
    
    # Returns an anime by name
    def AnimeByName(self, request, context):
        AnimeName = request.anime_name
        print("Searching for anime with name: ", AnimeName)
        # Create an Anime object TODO: Remove this part after testing
        for anime in self.Animes_Objects:
            if anime.name == AnimeName:
                return anime_by_name_Response(anime=anime)
        raise NotFound("Anime not found")
    
    def MultipleAnimeByName(self, request, context):
        print("Searching for multiple animes by name")
        result = []
        for anime in self.Animes_Objects:
            if anime.name in request.anime_names:
                result.append(anime)  # Use a list instead of a set
        return multiple_anime_by_name_Response(animes=result)
    
    # Returns all animes that belong to some of the given genres
    def AnimeRelatedByGenre(self, request, context):
        print("Searching for animes by genre")
        result = []  # Use a list instead of a set
        
        for anime in self.Animes_Objects:
            print(anime.genres)
            # Check if any genre in request.anime_genres matches a genre in anime.genres
            if any(genre in anime.genres for genre in request.anime_genres):
                result.append(anime)  # Add to the list
        return anime_by_genre_Response(animes=result)
    

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
