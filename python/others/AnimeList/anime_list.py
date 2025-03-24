import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from concurrent import futures

import grpc
import AnimeList_pb2_grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
from AnimeList_pb2 import (
    AnimeGenre,
    Anime,
    get_animes,
    get_animes_Response,
    anime_related_by_genre_Request,
    anime_related_by_genre_Response,
    anime_by_name_Request,
    anime_by_name_Response,
)

from services.Anime import AnimeService_pb2
from services.Anime import AnimeService_pb2_grpc

class AnimeService(AnimeList_pb2_grpc.AnimeListServicer):

    def GetAnimes(self, request, context):
        # Create a channel to the AnimeService
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = AnimeService_pb2_grpc.AnimeServiceStub(channel)
            try:
                # Call the GetAnimes method of the AnimeService
                response = stub.GetAnimes(AnimeService_pb2.get_animes())
                return get_animes_Response(animes=response.animes)
            except grpc.RpcError as e:
                context.abort(grpc.StatusCode.INTERNAL, str(e))


    def GetAnimeByName(self, request, context):
        return NotFound('Anime not found')
    
    def GetAnimeRelatedByGenre(self, request, context):
        return NotFound('Anime not found')

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    AnimeList_pb2_grpc.add_AnimeListServicer_to_server(
        AnimeService(), server
    )
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()