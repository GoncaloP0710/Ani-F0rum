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
    PublishInTopicResponsePub
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
        self.channel = grpc.insecure_channel('localhost:50062')  # Create a channel to the TopicRepository
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
            response = self.stub.CreateTopic(TopicRepository_pb2.CreateTopicRequest(request.topicname))
            return CreateTopicResponsePub(topicname=response.topicname)
        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
            return None
    
    def GetTopic(self, request, context):

        try:
            response = self.stub.GetTopic(TopicRepository_pb2.GetTopicRequest(request.topicname))
            return GetTopicResponsePub(topic=response.topic)
        except grpc.RpcError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
            return None
    
    def PublishInTopic(self, request, context):

        topic_name = request.topicname
        publication_name = request.publicationname
        content = request.content

        try:
            if isinstance(content, Message):

                micro_service_response = Topic()
                reponse = self.stub.PublishMessage(TopicRepository_pb2.PublishMessage(
                    topic_name,
                    publication_name,
                    content
                ))
                
            elif isinstance(content, Image):

                micro_service_response = Topic()
                reponse = self.stub.PublishImage(TopicRepository_pb2.PublishImage(
                    topic_name,
                    publication_name,
                    content
                ))
        
            else:
                raise "Invalid content of publication"

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

    print(PublishService().GetTopics(None, None))

    server.wait_for_termination()

if __name__ == "__main__":
    serve()