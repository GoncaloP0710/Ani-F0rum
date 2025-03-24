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
)

from python.services.Anime import AnimeService_pb2
from python.services.Anime import AnimeService_pb2_grpc

class AnimeService(AnimeListServicer):

    def GetAnimeRelatedByGenre(self, request, context):
        return NotFound('Anime not found')

    def GetUserWatchedAnime(self, request, context):
        # Create a channel to the AnimeService
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = AnimeService_pb2_grpc.AnimeServiceStub(channel)
            try:
                # Call the GetAnimes method of the AnimeService
                response = stub.GetAnimes(AnimeService_pb2.get_animes())
                return user_watched_anime_Response(animes=response.animes)
            except grpc.RpcError as e:
                context.abort(grpc.StatusCode.INTERNAL, str(e))
    

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_AnimeListServicer_to_server(
        AnimeService(), server
    )
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()