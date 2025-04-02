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
        request = Publisher_pb2.GetTopicsRequestPub() # Create a request
        
        try:  # Make the request
            print("Processing a GetTopics request")
            response = stub.GetTopics(request)

            print("Returning the response")
            return [
                {
                    "name": topic.topicname,
                    "subscribers": [
                        {
                            "name": subscriber.name
                        }
                        for subscriber in topic.subscribers
                    ],
                    "publications": [
                        {
                            "name": publication.name,
                            "topic_name": publication.topicname,
                            "message": {
                                "username": publication.message.username,
                                "content": publication.message.content
                            },
                            "images": {
                                "name": publication.images.name,
                                "username": publication.images.username
                            }
                        }
                        for publication in topic.publications
                    ]
                }
                for topic in response.topics
            ]
        except grpc.RpcError as e:
            return {"error": f"RPC failed: {e}"}, 500

# having an error where it doesn't recognize the argument
#    return function(*args, **kwargs)
#           ^^^^^^^^^^^^^^^^^^^^^^^^^
#TypeError: create() missing 1 required positional argument: 'topic'
def create(topic):

    request.get_data
    topicname = topic.get('name')
    print(topicname)

    with grpc.insecure_channel('localhost:50061') as channel: # Connect to the anime_list server
        stub = Publisher_pb2_grpc.PublisherStub(channel)
        request = Publisher_pb2.CreateTopicRequestPub(topicname=topicname) # Create a request
        
        try:  # Make the request
            response = stub.CreateTopic(request)
            print("Topic Created: " + response.topicname)
            return response.topicname  # Return the list of animes as JSON
        except grpc.RpcError as e:
            return {"error": f"RPC failed: {e}"}, 500

def get_topic(topic_name):

    with grpc.insecure_channel('localhost:50061') as channel: # Connect to the anime_list server
        stub = Publisher_pb2_grpc.PublisherStub(channel)
        request = Publisher_pb2.GetTopicRequestPub(topicname=topic_name) # Create a request

        try:  # Make the request
            print("Processing a GetTopic request")
            response = stub.GetTopic(request)
            print("Returning the response")
            print(response)
            topic = response.topic
            print(topic)
            return {
                "name": topic.topicname,
                "subscribers": [
                    {
                        "name": subscriber.name
                    }
                    for subscriber in topic.subscribers
                ],
                "publications": [
                    {
                        "name": publication.name,
                        "topic_name": publication.topicname,
                        "message": {
                            "username": publication.message.username,
                            "content": publication.message.content
                        },
                        "images": {
                            "name": publication.images.name,
                            "username": publication.images.username
                        }
                    }
                    for publication in topic.publications
                ]
            }
        except grpc.RpcError as e:
            return {"error": f"RPC failed: {e}"}, 500

# not tested, stuck in create_topic error
def publish(topicname, publicationname, username, content):

    with grpc.insecure_channel('localhost:50061') as channel: # Connect to the anime_list server
        stub = Publisher_pb2_grpc.PublisherStub(channel)
        request = Publisher_pb2.PublishInTopicRequestPub() # Create a request
        
        try:  # Make the request
            response = stub.Publish(request)
            print("Published: " + response.publicationname)
            return response.publicationname  # Return the list of animes as JSON
        except grpc.RpcError as e:
            return {"error": f"RPC failed: {e}"}, 500

def get_user_personalized():
    ...

def get_user_personalized_feed():
    ...

if __name__ == "__main__":
    connex_app.run(host="0.0.0.0", port=50060)
