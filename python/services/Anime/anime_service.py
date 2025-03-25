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
    anime_by_name_Response,
    get_multiple_anime_Response,
    anime_by_genre_Response,
)

from python.Common.Anime_pb2 import (
    Anime,
    AnimeGenre,
) 

from python.repository.Anime import AnimeRepository_pb2
from python.repository.Anime import AnimeRepository_pb2_grpc

class AnimeService_Service(AnimeServiceServicer):

    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50053')  # Create a channel to the AnimeRepository
        self.stub = AnimeRepository_pb2_grpc.AnimeRepositoryStub(self.channel)

    # Call the GetAnimes method of the AnimeRepository to get all animes
    def GetAnimes(self, request, context):
        try:
            response = self.stub.GetAnimes(AnimeRepository_pb2.get_animes())
            return get_animes_Response(animes=response.animes)
        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))

    # Call the GetAnimeByName method of the AnimeRepository to get an anime by name
    def GetAnimeByName(self, request, context):
        try:
            response = self.stub.GetAnimeByName(AnimeRepository_pb2.anime_by_name_Request(anime_name=request.anime_name))
            return anime_by_name_Response(anime=response.anime)
        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
    
    # Call multiple times the GetAnimeByName method of the AnimeRepository to get multiple animes by name
    def GetMultipleAnime(self, request, context):
        animeList = []
        try:
            for anime in request.anime_names:
                response = self.stub.GetAnimeByName(AnimeRepository_pb2.anime_by_name_Request(anime_name=anime))
                animeList.append(response.anime)
            return get_multiple_anime_Response(animes=animeList)
        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
    
    # Call the GetAnimeRelatedByGenre method of the AnimeRepository to get animes with the samme genre
    # TODO: Change it to recive a list of genres
    def GetAnimeByGenre(self, request, context):
        try:
            response = self.stub.GetAnimeRelatedByGenre(AnimeRepository_pb2.anime_by_genre_Request(anime_genre=request.anime_genre))
            return anime_by_genre_Response(animes=response.animes)
        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
    
def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_AnimeServiceServicer_to_server(
        AnimeService_Service(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("AnimeService server is running on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
