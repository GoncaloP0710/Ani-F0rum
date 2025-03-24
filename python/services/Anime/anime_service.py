from concurrent import futures

import grpc
import AnimeService_pb2_grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
from AnimeService_pb2 import (
    AnimeGenre,
    Anime,
    get_animes,
    get_animes_Response,
    anime_related_by_genre_Request,
    anime_related_by_genre_Response,
    anime_by_name_Request,
    anime_by_name_Response,
)

class AnimeService(AnimeService_pb2_grpc.AnimeServiceServicer):

    def GetAnimes(self, request, context):
        all_animes = [
            Anime(
                name="Naruto",
                genre="Shounen",
                episodes=220,
                rating=4.5,
                year=2002,
            ),
            Anime(
                name="One Piece",
                genre="Shounen",
                episodes=1000,
                rating=4.8,
                year=1999,
            ),
            Anime(
                name="Death Note",
                genre="Mystery",
                episodes=37,
                rating=4.7,
                year=2006,
            ),
            Anime(
                name="Attack on Titan",
                genre="Action",
                episodes=75,
                rating=4.9,
                year=2013,
            ),
        ]
        return get_animes_Response(animes=all_animes)

    def GetAnimeByName(self, request, context):
        return NotFound('Anime not found')
    
    def GetAnimeRelatedByGenre(self, request, context):
        return NotFound('Anime not found')
    
def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    AnimeService_pb2_grpc.add_AnimeServiceServicer_to_server(
        AnimeService(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("AnimeService server is running on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
