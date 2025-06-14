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

    with grpc.insecure_channel('publisher:50061') as channel: # Connect to the anime_list server
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

def create(topic_name):

    print('Handling a create request')

    with grpc.insecure_channel('publisher:50061') as channel: # Connect to the anime_list server
        stub = Publisher_pb2_grpc.PublisherStub(channel)
        print('Before request to other micro service')
        request = Publisher_pb2.CreateTopicRequestPub(topicname=topic_name) # Create a request
        
        try:  # Make the request
            response = stub.CreateTopic(request)
            print("Topic Created: " + response.topicname)
            return response.topicname  # Return the list of animes as JSON
        except grpc.RpcError as e:
            return {"error": f"RPC failed: {e}"}, 500

def get_topic(topic_name):

    with grpc.insecure_channel('publisher:50061') as channel: # Connect to the anime_list server
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

def publish(body):

    print('Handling a publish request')

    publication_name = body.get('name')
    topic_name = body.get('topic_name')
    message = body.get('message')
    images = body.get('images')
    content = None
    username = None
    image_name = None
    
    if message:
        content = message.get('content')
        username = message.get('username')
    else:
        username = images.get('username')
        image_name = images.get('name')


    with grpc.insecure_channel('publisher:50061') as channel: # Connect to the anime_list server
        stub = Publisher_pb2_grpc.PublisherStub(channel)

        request = None

        if message:
            request = Publisher_pb2.PublishInTopicRequestPub(
                topicname=topic_name,
                publicationname=publication_name,
                image=None,
                message=Topic_pb2.Message(
                    username=username,
                    content=content
                )
            )
        elif images:
            request = Publisher_pb2.PublishInTopicRequestPub(
                topicname=topic_name,
                publicationname=publication_name,
                image=Topic_pb2.Image(
                    username=username,
                    name=image_name
                ),
                message=None
            )
        
        else:
            return {"error": "Invalid content of publication"}, 400

        try:  # Make the request
            response = stub.Publish(request)
            print("Published: " + response.publicationname)
            return response.publicationname  # Return the list of animes as JSON
        except grpc.RpcError as e:
            return {"error": f"RPC failed: {e}"}, 500

def healthz():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    connex_app.run(host="0.0.0.0", port=50060)