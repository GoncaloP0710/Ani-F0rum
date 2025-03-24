import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from python.services.Anime.AnimeService_pb2_grpc import (
    AnimeServiceServicer,
    add_AnimeServiceServicer_to_server,
)
from python.services.Anime.AnimeService_pb2 import (
    get_animes_Response,
)

from python.Common.Anime_pb2 import (
    Anime,
    AnimeGenre,
) 

class AnimeService(AnimeServiceServicer):

    def GetAnimes(self, request, context):
        all_animes = [
            Anime(
                name='Naruto',
                genres=[AnimeGenre.ACTION],
                score=8.5,
                episodes=220,
                aired="2002-2007",
                synopsis="A young ninja strives to become the Hokage."
            ),
            Anime(
                name='One Piece',
                genres=[AnimeGenre.ACTION, AnimeGenre.ADVENTURE],
                score=8.7,
                episodes=1000,
                aired="1999-present",
                synopsis="A pirate's quest to find the ultimate treasure."
            ),
            Anime(
                name='Attack on Titan',
                genres=[AnimeGenre.ACTION, AnimeGenre.THRILLER],
                score=9.2,
                episodes=75,
                aired="2013-present",
                synopsis="Humanity fights for survival against giant humanoid Titans."
            ),
            Anime(
                name='Death Note',
                genres=[AnimeGenre.MYSTERY, AnimeGenre.THRILLER],
                score=9.0,
                episodes=37,
                aired="2006-2007",
                synopsis="A high school student discovers a supernatural notebook."
            ),
            Anime(
                name='My Hero Academia',
                genres=[AnimeGenre.ACTION],
                score=8.6,
                episodes=113,
                aired="2016-present",
                synopsis="A boy born without superpowers in a world where they are common."
            ),
            Anime(
                name='Tokyo Ghoul',
                genres=[AnimeGenre.HORROR, AnimeGenre.ACTION],
                score=8.0,
                episodes=48,
                aired="2014-2018",
                synopsis="A college student becomes a half-ghoul after a near-fatal encounter."
            ),
            Anime(
                name='Demon Slayer',
                genres=[AnimeGenre.ACTION, AnimeGenre.FANTASY],
                score=8.7,
                episodes=26,
                aired="2019",
                synopsis="A young boy becomes a demon slayer to avenge his family."
            ),
            Anime(
                name='Fullmetal Alchemist: Brotherhood',
                genres=[AnimeGenre.ACTION, AnimeGenre.FANTASY],
                score=9.1,
                episodes=64,
                aired="2009-2010",
                synopsis="Two brothers use alchemy in their quest to restore their bodies."
            ),
        ]
        return get_animes_Response(animes=all_animes)

    def GetAnimeByName(self, request, context):
        return NotFound('Anime not found')
    
    def GetMultipleAnime(self, request, context):
        return NotFound('Anime not found')
    
    def GetAnimeByGenre(self, request, context):
        return NotFound('Anime not found')
    
def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_AnimeServiceServicer_to_server(
        AnimeService(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("AnimeService server is running on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
