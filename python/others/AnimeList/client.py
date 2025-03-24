import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import grpc
from python.others.AnimeList import AnimeList_pb2_grpc, AnimeList_pb2

def run():
    # Connect to the anime_list server
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = AnimeList_pb2_grpc.AnimeListStub(channel)
        
        # Create a request
        request = AnimeList_pb2.user_watched_anime_Request(user_name = "Gajo")
        
        try:
            # Make the request
            response = stub.GetUserWatchedAnime(request)
            print(response)
        except grpc.RpcError as e:
            print(f"RPC failed: {e}")

if __name__ == '__main__':
    run()