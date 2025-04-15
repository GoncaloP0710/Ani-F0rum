import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import random
from concurrent import futures

import grpc

from python.others.Publisher.Publisher_pb2_grpc import (
    PublisherServicer,
    PublisherStub,
    add_PublisherServicer_to_server,
)

from python.others.Publisher.Publisher_pb2 import (
    # Responses
    GetTopicsResponsePub,
    CreateTopicResponsePub,
    GetTopicResponsePub,
    PublishInTopicResponsePub,
    # Requests
    PublishInTopicRequestPub,
)

from python.repository.Topic.TopicRepository_pb2_grpc import (
    TopicRepositoryStub
)

from python.Common.Topic_pb2 import (
    Subscriber,
    Message,
    Image,
    Publication,
    Topic,
)

from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from python.repository.Topic import TopicRepository_pb2
from python.repository.Topic import TopicRepository_pb2_grpc   

class PublishService(PublisherServicer):

    def __init__(self):
        self.channel = grpc.insecure_channel('topic-repository:50062')  # Create a channel to the TopicRepository
        self.stub = TopicRepositoryStub(self.channel)

    def GetTopics(self, request, context):

        try:
            print("Processing a GetTopics request")
            response = self.stub.GetTopics(TopicRepository_pb2.GetTopicsRequest())
            return GetTopicsResponsePub(topics=response.topics)
        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
            return None
    
    def CreateTopic(self, request, context):

        try:
            print("Processing a CreateTopics request")
            response = self.stub.CreateTopic(TopicRepository_pb2.CreateTopicRequest(topicname=request.topicname))
            return CreateTopicResponsePub(topicname=response.topicname)
        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
            return None
    
    def GetTopic(self, request, context):

        try:
            print("Processing a GetTopic request")
            response = self.stub.GetTopic(TopicRepository_pb2.GetTopicRequest(topicname=request.topicname))
            return GetTopicResponsePub(topic=response.topic)
        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
            return None
    
    def Publish(self, request, context):

        print("Processing a PublishInTopic request")
        print('Received request')
        print(request)

        topic_name = request.topicname
        publication_name = request.publicationname
        message = request.message
        image = request.image

        print('topicname')
        print(topic_name)
        print('publication_name')
        print(publication_name)

        response = None

        try:
            if message != None:

                micro_service_response = Topic()
    
                print('message user')
                print(message.username)
                print('message content')
                print(message.content)

                response = self.stub.PublishMessage(TopicRepository_pb2.PublishMessageInTopicRequest(
                    topicname=topic_name,
                    publicationname=publication_name,
                    message=Message(
                        username=message.username,
                        content=message.content
                    )
                ))
                
            elif image != None:

                print('image name')
                print(image.name)
                print('image username')
                print(image.username)

                micro_service_response = Topic()
                response = self.stub.PublishImage(TopicRepository_pb2.PublishImageInTopicRequest(
                    topicname=topic_name,
                    publicationname=publication_name,
                    image=Image(
                        name=image.name,
                        username=image.username
                    )
                ))
        
            else:
                raise "Invalid content of publication"

            print(response)

            return PublishInTopicResponsePub(publicationname=response.publicationname)
        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
            return None
    
"""
    def Recommend(self, request, context):
        if request.category not in books_by_category:
            raise NotFound("Category not found")

        books_for_category = books_by_category[request.category]
        num_results = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(books_for_category, num_results)

        return RecommendationResponse(publisher=books_to_recommend)
"""

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_PublisherServicer_to_server(
        PublishService(), server
    )

    """
    with open("server.key", "rb") as fp:
        server_key = fp.read()
    with open("server.pem", "rb") as fp:
        server_cert = fp.read()
    with open("ca.pem", "rb") as fp:
        ca_cert = fp.read()

    creds = grpc.ssl_server_credentials(
        [(server_key, server_cert)],
        root_certificates=ca_cert,
        require_client_auth=True,
    )
    """

    server.add_insecure_port("[::]:50061")
    print('Publisher server running on port 50061')
    server.start()

    #print (PublishService().CreateTopic(TopicRepository_pb2.CreateTopicRequest(topicname="Test"), None))
    #print (PublishService().GetTopic(TopicRepository_pb2.GetTopicRequest(topicname="Test"), None))
    #print (PublishService().PublishInTopic(PublishInTopicRequestPub(topicname="Solo Leveling ep12", publicationname="Test Message", message=Message(
    #    username="testUser1",
    #    content="This is a test"
    #)), None))
    #print (PublishService().PublishInTopic(PublishInTopicRequestPub(topicname="Solo Leveling ep12", publicationname="Test Image", image=Image(
    #    name="test image",
    #    username="testUser1"
    #)), None))

    server.wait_for_termination()

if __name__ == "__main__":
    serve()