import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import connexion
import pathlib

basedir = pathlib.Path(__file__).parent.resolve()

connex_app = connexion.App(__name__, specification_dir=basedir)
connex_app.add_api(basedir / "swagger.yml")

import grpc
from python.others.Publisher import Publisher_pb2_grpc, Publisher_pb2
from python.Common import Topic_pb2

def all_topics():

    with grpc.insecure_channel('localhost:50061') as channel: # Connect to the anime_list server
        stub = Publisher_pb2_grpc.PublisherStub(channel)
        request = Publisher_pb2.GetTopicsRequest() # Create a request
        
        try:  # Make the request
            response = stub.GetTopics(request)
            for topic in response.topics:
                print("Topic: " + topic)
            return [topic for topic in response.topics]  # Return the list of animes as JSON
        except grpc.RpcError as e:
            return {"error": f"RPC failed: {e}"}, 500

if __name__ == "__main__":
    connex_app.run(host="0.0.0.0", port=50060)
